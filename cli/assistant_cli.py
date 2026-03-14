import os
import ollama

from config.settings import DATA_DIR, LABS_DIR, KNOWLEDGE_BASE_DIR, ANALYSIS_DIR
from modules.doc_reader.reader import ler_arquivo, buscar_na_base, buscar_doc_em_data
from modules.official_docs.online_reader import buscar_doc_online
from modules.man_reader.reader import ler_man_page
from modules.lab_generator.generator import (
    gerar_lab,
    montar_prompt_lab,
    salvar_lab_arquivo as salvar_lab_arquivo_module,
)
from modules.code_analyzer.analyzer import (
    ler_codigo,
    analisar_texto,
    analisar_texto_stream,
    corrigir_texto_stream,
)

MAPA_DOCS = {
    "linux": "linux_docs",
    "git": "git_docs",
    "docker": "docker_docs",
    "terraform": "terraform_docs",
    "kubernetes": "kubernetes_docs",
    "aws": "aws_docs",
}

ULTIMO_WEBDOC = {
    "tecnologia": None,
    "assunto": None,
    "url": None,
    "conteudo": None,
    "resposta": None,
}


def limpar_tokens(texto):
    texto = texto.replace("<｜begin▁of▁sentence｜>", "")
    texto = texto.replace("<｜end▁of▁sentence｜>", "")
    return texto


def gerar_resposta(modelo_escolhido, mensagens):
    try:
        stream = ollama.chat(
            model=modelo_escolhido,
            messages=mensagens,
            stream=True,
            options={
                "temperature": 0.2,
                "num_predict": 2500,
            },
        )

        resposta_completa = ""

        for parte in stream:
            texto_parte = parte["message"]["content"]

            if not texto_parte:
                continue

            texto_parte = limpar_tokens(texto_parte)
            resposta_completa += texto_parte
            print(texto_parte, end="", flush=True)

        print()
        return resposta_completa.strip()

    except Exception as erro:
        mensagem = f"Erro ao usar o modelo '{modelo_escolhido}': {erro}"
        print(mensagem)
        return ""


def escolher_modelo():
    print("DevOps Assistant iniciado")
    print("\nEscolha o modelo:\n")

    print("1 - deepseek-coder:6.7b")
    print("    Melhor para: análise de código, DevOps, Terraform, Docker, Kubernetes\n")

    print("2 - deepseek-coder:6.7b-ctx4k")
    print("    Melhor para: arquivos grandes, YAML grande, projetos maiores\n")

    print("3 - qwen2.5-coder:1.5b-base")
    print("    Melhor para: respostas rápidas, perguntas simples e estudo\n")

    opcao = input("Digite o número do modelo: ").strip()

    if opcao == "1":
        modelo = "deepseek-coder:6.7b"
    elif opcao == "2":
        modelo = "deepseek-coder:6.7b-ctx4k"
    elif opcao == "3":
        modelo = "qwen2.5-coder:1.5b-base"
    else:
        print("Modelo inválido, usando deepseek padrão")
        modelo = "deepseek-coder:6.7b"

    print(f"\nUsando modelo: {modelo}\n")
    return modelo


def mostrar_comandos():
    print("Comandos disponíveis:\n")
    print("analisar:arquivo              → analisar código ou configuração")
    print("corrigir:arquivo              → corrigir código ou configuração")
    print("doc:linux/comando             → ler documentação local")
    print("melhorar doc:linux/comando    → melhorar documentação local")
    print("webdoc:git/comando            → consultar documentação oficial")
    print("man:comando                   → consultar man page")
    print("refazer                       → refazer última explicação oficial")
    print("salvar base:topico            → salvar conteúdo na knowledge-base")
    print("lab:linux/comando             → gerar laboratório prático")
    print("lab:list                      → listar labs salvos\n")
    print("Digite sua pergunta ou 'sair' para encerrar\n")


def montar_prompt_webdoc(url, conteudo_online, tentativa_refazer=False):
    titulo = "Explique NOVAMENTE" if tentativa_refazer else "Explique"

    system_prompt = f"""Você é um professor DevOps experiente.

{titulo} o conteúdo da documentação oficial de forma amigável, leve e didática.

REGRAS IMPORTANTES:
- Responda em português do Brasil.
- Faça uma explicação friendly, como um professor ensinando alguém que está estudando.
- Foque no que o comando, recurso ou serviço FAZ.
- Ignore listas grandes de opções e parâmetros.
- Ignore blocos muito crus da documentação.
- Não copie trechos longos literalmente.
- Não invente comandos nem informações fora do conteúdo.
- Priorize clareza em vez de excesso de detalhes.

Estrutura da resposta:

1. O que é
2. Explicação simples
3. Exemplo prático
4. Quando usar
5. Observação importante
"""

    user_prompt = f"""
Fonte oficial:
{url}

Documentação oficial:
{conteudo_online}
"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def resolver_caminho_analise(caminho_arquivo):
    if os.path.isabs(caminho_arquivo):
        return caminho_arquivo

    return os.path.join(ANALYSIS_DIR, os.path.basename(caminho_arquivo))


def atualizar_ultimo_webdoc(
    tecnologia=None, assunto=None, url=None, conteudo=None, resposta=None
):
    ULTIMO_WEBDOC["tecnologia"] = tecnologia
    ULTIMO_WEBDOC["assunto"] = assunto
    ULTIMO_WEBDOC["url"] = url
    ULTIMO_WEBDOC["conteudo"] = conteudo
    ULTIMO_WEBDOC["resposta"] = resposta


def salvar_lab_arquivo(assunto, conteudo_lab):
    resultado = salvar_lab_arquivo_module(assunto, conteudo_lab, modo="fail")

    if resultado["status"] == "saved":
        print(f"\nLab salvo em: {resultado['caminho']}\n")
        return

    if resultado["status"] == "exists":
        print(f"\nO lab {resultado['caminho']} já existe.\n")
        print("1 - Sobrescrever")
        print("2 - Salvar com outro nome")
        print("3 - Cancelar")

        escolha = input("\nEscolha uma opção: ").strip()

        if escolha == "1":
            resultado = salvar_lab_arquivo_module(
                assunto, conteudo_lab, modo="overwrite"
            )

            if resultado["status"] == "saved":
                print(f"\nLab salvo em: {resultado['caminho']}\n")
            else:
                print("\nErro ao sobrescrever o lab.\n")

            return

        if escolha == "2":
            novo_nome = input("Digite o novo nome do lab (sem .md): ").strip().lower()

            resultado = salvar_lab_arquivo_module(
                assunto, conteudo_lab, modo="rename", novo_nome=novo_nome
            )

            if resultado["status"] == "saved":
                print(f"\nLab salvo em: {resultado['caminho']}\n")
            elif resultado["status"] == "exists":
                print(f"\nJá existe um lab com esse nome: {resultado['caminho']}\n")
            else:
                print(f"\nErro: {resultado.get('message', 'erro ao salvar lab')}\n")

            return

        print("Operação cancelada.")
        return

    print(f"\nErro: {resultado.get('message', 'erro ao salvar lab')}\n")


def obter_doc_local(comando_doc):
    caminho_arquivo = None
    conteudo = None

    if "/" in comando_doc:
        tecnologia, arquivo = comando_doc.split("/", 1)

        tecnologia = tecnologia.strip().lower()
        arquivo = arquivo.strip().lower()

        if tecnologia not in MAPA_DOCS:
            print(
                "Tecnologia não encontrada. Use: linux, git, docker, terraform, kubernetes ou aws."
            )
            return None, None

        base = os.path.join(DATA_DIR, MAPA_DOCS[tecnologia], arquivo)

        if os.path.exists(base + ".md"):
            caminho_arquivo = base + ".md"
        elif os.path.exists(base + ".txt"):
            caminho_arquivo = base + ".txt"
        else:
            raise FileNotFoundError

        conteudo = ler_arquivo(caminho_arquivo)
        return caminho_arquivo, conteudo

    caminho_arquivo, conteudo = buscar_doc_em_data(comando_doc)
    return caminho_arquivo, conteudo


def listar_labs():
    pasta_labs = LABS_DIR

    if not os.path.exists(pasta_labs):
        print("Nenhum lab encontrado.")
        return

    print("\nLABS DISPONÍVEIS\n")

    contador = 1
    mapa_labs = {}

    for tecnologia in sorted(os.listdir(pasta_labs)):
        caminho_tecnologia = os.path.join(pasta_labs, tecnologia)

        if not os.path.isdir(caminho_tecnologia):
            continue

        print(tecnologia)

        for arquivo in sorted(os.listdir(caminho_tecnologia)):
            if arquivo.endswith(".md"):
                nome_lab = arquivo.replace(".md", "")
                print(f"  {contador} - {nome_lab}")
                mapa_labs[str(contador)] = f"{tecnologia}/{nome_lab}"
                contador += 1

    escolha = input(
        "\nDigite o número do lab para abrir ou pressione Enter para sair: "
    ).strip()

    if escolha in mapa_labs:
        tecnologia, nome_lab = mapa_labs[escolha].split("/")
        caminho = os.path.join(LABS_DIR, tecnologia, f"{nome_lab}.md")
        conteudo = ler_arquivo(caminho)

        print(f"\n[Lab encontrado: {caminho}]\n")
        print(conteudo)


def salvar_base(pergunta):
    if not ULTIMO_WEBDOC["resposta"]:
        print("Nenhuma explicação recente para salvar.")
        return

    try:
        comando = pergunta.replace("salvar base:", "").strip()
        tecnologia, assunto = comando.split("/")

        tecnologia = tecnologia.strip().lower()
        assunto = assunto.strip().lower()

        pasta_destino = os.path.join(KNOWLEDGE_BASE_DIR, tecnologia, "explanations")
        os.makedirs(pasta_destino, exist_ok=True)

        arquivo_destino = os.path.join(pasta_destino, f"{assunto}.md")

        with open(arquivo_destino, "w", encoding="utf-8") as f:
            f.write(f"# {assunto}\n\n")
            f.write("## Fonte\n")
            f.write(f"{ULTIMO_WEBDOC['url']}\n\n")
            f.write("## Explicação\n\n")
            f.write(ULTIMO_WEBDOC["resposta"])

        print(f"\nBase salva em: {arquivo_destino}\n")

    except Exception as erro:
        print(f"Erro ao salvar base: {erro}")


def processar_doc(pergunta):
    try:
        comando_doc = pergunta[4:].strip()
        caminho_arquivo, conteudo = obter_doc_local(comando_doc)

        if not caminho_arquivo:
            print("Documentação não encontrada em data/.")
            return

        print(f"\n[Documentação local encontrada: {caminho_arquivo}]\n")
        print(conteudo)
        print()

    except ValueError:
        print("Formato inválido. Use algo como: doc:linux/mkdir")
    except FileNotFoundError:
        print("Arquivo de documentação não encontrado.")


def processar_verificar_doc(pergunta, modelo):
    assunto = pergunta.replace("verificar doc:", "").strip()

    caminho_encontrado, conteudo_base = buscar_na_base(assunto)

    if not caminho_encontrado:
        print("Assunto não encontrado na base local.")
        return

    print(f"\n[Base local encontrada: {caminho_encontrado}]\n")

    mensagens = [
        {
            "role": "system",
            "content": """Você é um especialista DevOps e arquiteto cloud.

Sua tarefa é AUDITAR a base de conhecimento do usuário.

IMPORTANTE:
- NÃO reescreva o conteúdo.
- NÃO copie o texto da base.
- NÃO traduza a base.
- NÃO gere um artigo novo.

Você deve apenas analisar a base e responder:

1. Se o conteúdo está tecnicamente correto
2. O que está faltando segundo boas práticas atuais
3. Se existe algo desatualizado
4. Sugestões curtas de melhoria

Se a base estiver correta, diga apenas que está correta.""",
        },
        {
            "role": "user",
            "content": f"""
Base atual:

{conteudo_base}

Assunto:
{assunto}

Compare com documentação atual e boas práticas.
""",
        },
    ]

    gerar_resposta(modelo, mensagens)


def processar_melhorar_doc(pergunta, modelo):
    assunto = pergunta.replace("melhorar doc:", "").strip()

    caminho_doc, conteudo_doc = buscar_doc_em_data(assunto)

    if not caminho_doc:
        print("Documentação não encontrada em data/.")
        return

    print(f"\n[Documentação encontrada em data: {caminho_doc}]\n")

    mensagens = [
        {
            "role": "system",
            "content": """Você é um professor DevOps.

Sua tarefa é melhorar a explicação da documentação fornecida.

REGRAS:
- Responda em português.
- Seja claro, direto e didático.
- Explique somente o conteúdo da documentação.
- Não invente comandos que não estejam relacionados ao assunto.
- Organize a resposta em:
1. O que é ou o que faz
2. Explicação simples
3. Exemplo prático
4. Casos de uso
""",
        },
        {
            "role": "user",
            "content": f"""
Assunto: {assunto}

Documentação:
{conteudo_doc}
""",
        },
    ]

    gerar_resposta(modelo, mensagens)


def processar_man(pergunta, modelo):
    comando = pergunta.replace("man:", "").strip()

    try:
        conteudo_man, erro = ler_man_page(comando)

        if erro:
            print(erro)
            return

        mensagens = [
            {
                "role": "system",
                "content": """Você é um professor de Linux.

Explique a man page de forma didática.

REGRAS IMPORTANTES:
- Responda em português.
- Use formatação Markdown.
- Cada seção deve começar em uma nova linha.
- Sempre deixe uma linha em branco entre seções.
- Não escreva tudo em um único parágrafo.
- Não escreva assinaturas ou despedidas.
- Não escreva frases como "fim da explicação".

Estrutura obrigatória:

## O que o comando faz

## Sintaxe básica

## Principais opções

## Exemplos práticos
""",
            },
            {"role": "user", "content": conteudo_man},
        ]

        resposta = gerar_resposta(modelo, mensagens)
        atualizar_ultimo_webdoc(
            tecnologia="linux",
            assunto=comando,
            url=f"man:{comando}",
            conteudo=conteudo_man,
            resposta=resposta,
        )

    except Exception as erro:
        print(f"Erro ao consultar man page: {erro}")


def processar_webdoc(pergunta, modelo):
    try:
        comando_webdoc = pergunta[7:]
        tecnologia, assunto = comando_webdoc.split("/")
        tecnologia = tecnologia.strip().lower()
        assunto = assunto.strip().lower()
    except ValueError:
        print("Formato inválido. Use algo como: webdoc:git/clone")
        return

    url, conteudo_online, erro = buscar_doc_online(pergunta)

    if erro:
        print(f"Erro ao consultar documentação online: {erro}")
        return

    atualizar_ultimo_webdoc(
        tecnologia=tecnologia,
        assunto=assunto,
        url=url,
        conteudo=conteudo_online,
        resposta=None,
    )

    print(f"\n[Documentação oficial online encontrada: {url}]\n")

    mensagens = montar_prompt_webdoc(url, conteudo_online, tentativa_refazer=False)
    resposta = gerar_resposta(modelo, mensagens)
    ULTIMO_WEBDOC["resposta"] = resposta


def processar_refazer(modelo):
    if not ULTIMO_WEBDOC["conteudo"]:
        print("Nenhum webdoc recente para refazer.")
        return

    print("\n[Refazendo explicação com base na mesma documentação oficial]\n")

    mensagens = montar_prompt_webdoc(
        ULTIMO_WEBDOC["url"],
        ULTIMO_WEBDOC["conteudo"],
        tentativa_refazer=True,
    )

    resposta = gerar_resposta(modelo, mensagens)
    ULTIMO_WEBDOC["resposta"] = resposta


def processar_lab(pergunta, modelo):
    assunto = pergunta.replace("lab:", "").strip()

    if not assunto:
        print("Informe um assunto para gerar o lab. Exemplo: lab:linux/mkdir")
        return

    resultado_lab = gerar_lab(
        assunto,
        buscar_na_base,
        buscar_doc_em_data,
    )

    fonte_tipo = resultado_lab["fonte_tipo"]
    fonte_caminho = resultado_lab["fonte_caminho"]
    contexto = resultado_lab["conteudo"]

    if fonte_caminho:
        print(f"\n[Gerando lab com base em: {fonte_caminho}]\n")
    else:
        print("\n[Gerando lab com base no assunto informado]\n")

    print("Fonte usada:")
    print(f"Tipo: {fonte_tipo}")

    if fonte_caminho:
        print(f"Caminho: {fonte_caminho}")

    mensagens = montar_prompt_lab(
        assunto=assunto,
        contexto=contexto,
        fonte_tipo=fonte_tipo,
        fonte_caminho=fonte_caminho,
    )

    resposta = gerar_resposta(modelo, mensagens)

    atualizar_ultimo_webdoc(
        tecnologia=None,
        assunto=assunto,
        url=fonte_caminho if fonte_caminho else f"lab:{assunto}",
        conteudo=contexto,
        resposta=resposta,
    )

    salvar = input("\nDeseja salvar este lab? (s/n): ").strip().lower()
    if salvar == "s":
        salvar_lab_arquivo(assunto, resposta)


def processar_analisar(pergunta, modelo):
    caminho_arquivo = pergunta.replace("analisar:", "").strip()

    if not caminho_arquivo:
        print("Informe o caminho do arquivo. Exemplo: analisar:teste.sh")
        return

    caminho_arquivo = resolver_caminho_analise(caminho_arquivo)
    conteudo_codigo, erro = ler_codigo(caminho_arquivo)

    if erro:
        print(erro)
        return

    print(f"\n[Analisando arquivo: {caminho_arquivo}]\n")

    gerou_saida = False

    for chunk in analisar_texto_stream(modelo, caminho_arquivo, conteudo_codigo):
        if not chunk:
            continue

        print(chunk, end="", flush=True)
        gerou_saida = True

    if gerou_saida:
        print()
    else:
        print("Nenhuma resposta foi gerada.")


def processar_corrigir(pergunta, modelo):
    caminho_arquivo = pergunta.replace("corrigir:", "").strip()

    if not caminho_arquivo:
        print("Informe o caminho do arquivo. Exemplo: corrigir:teste.sh")
        return

    caminho_arquivo = resolver_caminho_analise(caminho_arquivo)
    conteudo_codigo, erro = ler_codigo(caminho_arquivo)

    if erro:
        print(erro)
        return

    print(f"\n[Corrigindo arquivo: {caminho_arquivo}]\n")

    gerou_saida = False

    for chunk in corrigir_texto_stream(modelo, caminho_arquivo, conteudo_codigo):
        if not chunk:
            continue

        print(chunk, end="", flush=True)
        gerou_saida = True

    if gerou_saida:
        print()
    else:
        print("Nenhuma resposta foi gerada.")


def processar_pergunta_livre(pergunta, modelo):
    caminho_encontrado, conteudo_base = buscar_na_base(pergunta)

    if caminho_encontrado:
        nome_arquivo = os.path.basename(caminho_encontrado).replace(".md", "").lower()

        if nome_arquivo in pergunta.lower():
            print(f"\n[Base local encontrada: {caminho_encontrado}]\n")
            print(conteudo_base)
            print()
            return

    mensagens = [{"role": "user", "content": pergunta}]
    gerar_resposta(modelo, mensagens)


def main():
    modelo = escolher_modelo()
    mostrar_comandos()

    while True:
        pergunta = input("> ").strip()

        if pergunta.lower() == "sair":
            print("Encerrando assistente...")
            break

        if not pergunta:
            print("Digite uma pergunta.")
            continue

        if pergunta.lower().startswith("doc:"):
            processar_doc(pergunta)
        elif pergunta.lower().startswith("verificar doc:"):
            processar_verificar_doc(pergunta, modelo)
        elif pergunta.lower().startswith("melhorar doc:"):
            processar_melhorar_doc(pergunta, modelo)
        elif pergunta.lower().startswith("man:"):
            processar_man(pergunta, modelo)
        elif pergunta.lower().startswith("webdoc:"):
            processar_webdoc(pergunta, modelo)
        elif pergunta.lower() == "refazer":
            processar_refazer(modelo)
        elif pergunta.lower().startswith("salvar base:"):
            salvar_base(pergunta)
        elif pergunta.lower() == "lab:list":
            listar_labs()
        elif pergunta.lower().startswith("lab:"):
            processar_lab(pergunta, modelo)
        elif pergunta.lower().startswith("analisar:"):
            processar_analisar(pergunta, modelo)
        elif pergunta.lower().startswith("corrigir:"):
            processar_corrigir(pergunta, modelo)
        else:
            processar_pergunta_livre(pergunta, modelo)


if __name__ == "__main__":
    main()
