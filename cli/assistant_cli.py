import os
import ollama
from modules.doc_reader.reader import ler_arquivo, buscar_na_base, buscar_doc_em_data
from modules.official_docs.online_reader import buscar_doc_online
from modules.man_reader.reader import ler_man_page
from modules.lab_generator.generator import gerar_lab, montar_prompt_lab
from modules.code_analyzer.analyzer import (
    ler_codigo,
    montar_prompt_analise,
    montar_prompt_correcao
)


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

print(f"\nUsando modelo: {modelo}")
print("Digite sua pergunta ou 'sair' para encerrar")
print("Para analisar código ou configuração. Exemplo: analisar:./Dockerfile")
print("Para ler documentação local. Exemplo: doc:linux/mkdir")
print("Para melhorar uma doc local. Exemplo: melhorar doc:linux/mkdir")
print("Para consultar documentação oficial. Exemplo: webdoc:git/clone")
print("Para consultar man page. Exemplo: man:mkdir")
print("Para refazer a última explicação oficial: refazer")
print("Para salvar na base. Exemplo: salvar base:git/clone")
print("Para gerar um lab. Exemplo: lab:linux/mkdir")
print("Para listar labs salvos: lab:list\n")


mapa_docs = {
    "linux": "linux_docs",
    "git": "git_docs",
    "docker": "docker_docs",
    "terraform": "terraform_docs",
    "kubernetes": "kubernetes_docs",
    "aws": "aws_docs"
}

ultimo_webdoc = {
    "tecnologia": None,
    "assunto": None,
    "url": None,
    "conteudo": None,
    "resposta": None
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
                "num_predict": 2500
            }
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


def montar_prompt_webdoc(url, conteudo_online, tentativa_refazer=False):
    if tentativa_refazer:
        system_prompt = """Você é um professor DevOps experiente.

Explique NOVAMENTE o conteúdo da documentação oficial de forma mais amigável, leve e didática.

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
    else:
        system_prompt = """Você é um professor DevOps experiente.

Explique a documentação oficial de forma amigável, leve e didática.

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
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]


def salvar_lab_arquivo(assunto, conteudo_lab):
    partes = assunto.split("/", 1)

    if len(partes) == 2:
        tecnologia, nome_lab = partes
        tecnologia = tecnologia.strip().lower()
        nome_lab = nome_lab.strip().lower()
    else:
        tecnologia = "geral"
        nome_lab = assunto.strip().lower().replace(" ", "-")

    pasta_destino = f"labs/{tecnologia}"
    os.makedirs(pasta_destino, exist_ok=True)

    arquivo_destino = f"{pasta_destino}/{nome_lab}.md"

    if os.path.exists(arquivo_destino):

        print(f"\nO lab {arquivo_destino} já existe.\n")
        print("1 - Sobrescrever")
        print("2 - Salvar com outro nome")
        print("3 - Cancelar")

        escolha = input("\nEscolha uma opção: ").strip()

        if escolha == "1":
            pass

        elif escolha == "2":
            novo_nome = input("Digite o novo nome do lab (sem .md): ").strip().lower()
            arquivo_destino = f"{pasta_destino}/{novo_nome}.md"

        else:
            print("Operação cancelada.")
            return

    with open(arquivo_destino, "w", encoding="utf-8") as f:
        f.write(conteudo_lab)

    print(f"\nLab salvo em: {arquivo_destino}\n")

while True:
    pergunta = input("> ").strip()

    if pergunta.lower() == "sair":
        print("Encerrando assistente...")
        break

    if not pergunta:
        print("Digite uma pergunta.")
        continue

    if pergunta.lower().startswith("doc:"):
        try:
            comando_doc = pergunta[4:].strip()

            caminho_arquivo = None
            conteudo = None

            if "/" in comando_doc:
                tecnologia, arquivo = comando_doc.split("/", 1)

                tecnologia = tecnologia.strip().lower()
                arquivo = arquivo.strip().lower()

                if tecnologia not in mapa_docs:
                    print("Tecnologia não encontrada. Use: linux, git, docker, terraform, kubernetes ou aws.")
                    continue

                base = f"data/{mapa_docs[tecnologia]}/{arquivo}"

                if os.path.exists(base + ".md"):
                    caminho_arquivo = base + ".md"
                elif os.path.exists(base + ".txt"):
                    caminho_arquivo = base + ".txt"
                else:
                    raise FileNotFoundError

                conteudo = ler_arquivo(caminho_arquivo)

            else:
                caminho_arquivo, conteudo = buscar_doc_em_data(comando_doc)

                if not caminho_arquivo:
                    print("Documentação não encontrada em data/.")
                    continue

            print(f"\n[Documentação local encontrada: {caminho_arquivo}]\n")
            print(conteudo)
            print()

        except ValueError:
            print("Formato inválido. Use algo como: doc:linux/mkdir")
            continue
        except FileNotFoundError:
            print("Arquivo de documentação não encontrado.")
            continue

    elif pergunta.lower().startswith("verificar doc:"):
        assunto = pergunta.replace("verificar doc:", "").strip()

        caminho_encontrado, conteudo_base = buscar_na_base(assunto)

        if not caminho_encontrado:
            print("Assunto não encontrado na base local.")
            continue

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

Se a base estiver correta, diga apenas que está correta."""
            },
            {
                "role": "user",
                "content": f"""
Base atual:

{conteudo_base}

Assunto:
{assunto}

Compare com documentação atual e boas práticas.
"""
            }
        ]

        gerar_resposta(modelo, mensagens)

    elif pergunta.lower().startswith("melhorar doc:"):
        assunto = pergunta.replace("melhorar doc:", "").strip()

        caminho_doc, conteudo_doc = buscar_doc_em_data(assunto)

        if not caminho_doc:
            print("Documentação não encontrada em data/.")
            continue

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
"""
            },
            {
                "role": "user",
                "content": f"""
Assunto: {assunto}

Documentação:
{conteudo_doc}
"""
            }
        ]

        gerar_resposta(modelo, mensagens)

    elif pergunta.lower().startswith("man:"):
        comando = pergunta.replace("man:", "").strip()

        try:
            conteudo_man, erro = ler_man_page(comando)

            if erro:
                print(erro)
                continue

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
"""
                },
                {
                    "role": "user",
                    "content": conteudo_man
                }
            ]

            resposta = gerar_resposta(modelo, mensagens)
            ultimo_webdoc["resposta"] = resposta
            ultimo_webdoc["url"] = f"man:{comando}"
            ultimo_webdoc["conteudo"] = conteudo_man
            ultimo_webdoc["tecnologia"] = "linux"
            ultimo_webdoc["assunto"] = comando

        except Exception as erro:
            print(f"Erro ao consultar man page: {erro}")
            continue

    elif pergunta.lower().startswith("webdoc:"):
        try:
            comando_webdoc = pergunta[7:]
            tecnologia, assunto = comando_webdoc.split("/")
            tecnologia = tecnologia.strip().lower()
            assunto = assunto.strip().lower()
        except ValueError:
            print("Formato inválido. Use algo como: webdoc:git/clone")
            continue

        url, conteudo_online, erro = buscar_doc_online(pergunta)

        if erro:
            print(f"Erro ao consultar documentação online: {erro}")
            continue

        ultimo_webdoc["tecnologia"] = tecnologia
        ultimo_webdoc["assunto"] = assunto
        ultimo_webdoc["url"] = url
        ultimo_webdoc["conteudo"] = conteudo_online
        ultimo_webdoc["resposta"] = None

        print(f"\n[Documentação oficial online encontrada: {url}]\n")

        mensagens = montar_prompt_webdoc(url, conteudo_online, tentativa_refazer=False)
        resposta = gerar_resposta(modelo, mensagens)
        ultimo_webdoc["resposta"] = resposta

    elif pergunta.lower() == "refazer":
        if not ultimo_webdoc["conteudo"]:
            print("Nenhum webdoc recente para refazer.")
            continue

        print("\n[Refazendo explicação com base na mesma documentação oficial]\n")

        mensagens = montar_prompt_webdoc(
            ultimo_webdoc["url"],
            ultimo_webdoc["conteudo"],
            tentativa_refazer=True
        )

        resposta = gerar_resposta(modelo, mensagens)
        ultimo_webdoc["resposta"] = resposta

    elif pergunta.lower().startswith("salvar base:"):
        if not ultimo_webdoc["resposta"]:
            print("Nenhuma explicação recente para salvar.")
            continue

        try:
            comando = pergunta.replace("salvar base:", "").strip()
            tecnologia, assunto = comando.split("/")

            tecnologia = tecnologia.strip().lower()
            assunto = assunto.strip().lower()

            pasta_destino = f"knowledge-base/{tecnologia}/explanations"
            os.makedirs(pasta_destino, exist_ok=True)

            arquivo_destino = f"{pasta_destino}/{assunto}.md"

            with open(arquivo_destino, "w", encoding="utf-8") as f:
                f.write(f"# {assunto}\n\n")
                f.write("## Fonte\n")
                f.write(f"{ultimo_webdoc['url']}\n\n")
                f.write("## Explicação\n\n")
                f.write(ultimo_webdoc["resposta"])

            print(f"\nBase salva em: {arquivo_destino}\n")

        except Exception as erro:
            print(f"Erro ao salvar base: {erro}")

    elif pergunta.lower() == "lab:list":
        pasta_labs = "labs"

        if not os.path.exists(pasta_labs):
            print("Nenhum lab encontrado.")
            continue

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

        escolha = input("\nDigite o número do lab para abrir ou pressione Enter para sair: ").strip()

        if escolha in mapa_labs:
            tecnologia, nome_lab = mapa_labs[escolha].split("/")
            caminho = f"labs/{tecnologia}/{nome_lab}.md"

            conteudo = ler_arquivo(caminho)

            print(f"\n[Lab encontrado: {caminho}]\n")
            print(conteudo)
    
    elif pergunta.lower().startswith("lab:"):
        assunto = pergunta.replace("lab:", "").strip()

        if not assunto:
            print("Informe um assunto para gerar o lab. Exemplo: lab:linux/mkdir")
            continue

        resultado_lab = gerar_lab(
            assunto,
            buscar_na_base,
            buscar_doc_em_data
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
            fonte_caminho=fonte_caminho
        )

        resposta = gerar_resposta(modelo, mensagens)

        ultimo_webdoc["resposta"] = resposta
        ultimo_webdoc["url"] = fonte_caminho if fonte_caminho else f"lab:{assunto}"
        ultimo_webdoc["conteudo"] = contexto
        ultimo_webdoc["tecnologia"] = None
        ultimo_webdoc["assunto"] = assunto

        salvar = input("\nDeseja salvar este lab? (s/n): ").strip().lower()
        if salvar == "s":
            salvar_lab_arquivo(assunto, resposta)

    elif pergunta.lower().startswith("analisar:"):
        caminho_arquivo = pergunta.replace("analisar:", "").strip()

        if not caminho_arquivo:
            print("Informe o caminho do arquivo. Exemplo: analisar:./Dockerfile")
            continue

        conteudo_codigo, erro = ler_codigo(caminho_arquivo)

        if erro:
            print(erro)
            continue

        print(f"\n[Analisando arquivo: {caminho_arquivo}]\n")

        mensagens = montar_prompt_analise(caminho_arquivo, conteudo_codigo)

        gerar_resposta(modelo, mensagens)

    elif pergunta.lower().startswith("corrigir:"):
        caminho_arquivo = pergunta.replace("corrigir:", "").strip()

        if not caminho_arquivo:
            print("Informe o caminho do arquivo. Exemplo: corrigir:analysis/teste.sh")
            continue

        conteudo_codigo, erro = ler_codigo(caminho_arquivo)

        if erro:
            print(erro)
            continue

        print(f"\n[Corrigindo arquivo: {caminho_arquivo}]\n")

        mensagens = montar_prompt_correcao(caminho_arquivo, conteudo_codigo)

        gerar_resposta(modelo, mensagens)

    else:
        caminho_encontrado, conteudo_base = buscar_na_base(pergunta)

        if caminho_encontrado:
            nome_arquivo = os.path.basename(caminho_encontrado).replace(".md", "").lower()

            if nome_arquivo in pergunta.lower():
                print(f"\n[Base local encontrada: {caminho_encontrado}]\n")
                print(conteudo_base)
                print()
                continue

        mensagens = [
            {"role": "user", "content": pergunta}
        ]

        gerar_resposta(modelo, mensagens)