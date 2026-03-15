import os
import re
import ollama


def ler_arquivo(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        return arquivo.read()


def normalizar_texto(texto):
    texto = texto.lower().strip()
    texto = re.sub(r"[^a-z0-9\s\-]", " ", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto
def buscar_na_base(pergunta, base_path="knowledge-base"):
    pergunta_normalizada = normalizar_texto(pergunta)
    palavras_pergunta = pergunta_normalizada.split()

    melhor_caminho = None
    melhor_conteudo = None
    melhor_score = 0

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".md"):
                caminho = os.path.join(root, file)

                try:
                    with open(caminho, "r", encoding="utf-8") as f:
                        conteudo_original = f.read()
                except Exception:
                    continue

                nome_arquivo = file.replace(".md", "")
                nome_normalizado = normalizar_texto(nome_arquivo)
                conteudo_normalizado = normalizar_texto(conteudo_original[:3000])

                score = 0

                for palavra in palavras_pergunta:
                    if palavra in nome_normalizado:
                        score += 3
                    if palavra in conteudo_normalizado:
                        score += 1

                if score > melhor_score:
                    melhor_score = score
                    melhor_caminho = caminho
                    melhor_conteudo = conteudo_original

    if melhor_score > 0:
        return melhor_caminho, melhor_conteudo

    return None, None

def buscar_doc_em_data(pergunta, data_path="data"):
    mapa_docs = {
        "linux": "linux_docs",
        "git": "git_docs",
        "docker": "docker_docs",
        "terraform": "terraform_docs",
        "kubernetes": "kubernetes_docs",
        "aws": "aws_docs",
    }

    pergunta = pergunta.strip().lower()

    if "/" in pergunta:
        try:
            tecnologia, arquivo = pergunta.split("/", 1)
            tecnologia = tecnologia.strip()
            arquivo = arquivo.strip()

            if tecnologia in mapa_docs:
                caminho = os.path.join(
                    data_path, mapa_docs[tecnologia], f"{arquivo}.md"
                )

                if os.path.exists(caminho):
                    return caminho, ler_arquivo(caminho)
        except Exception:
            pass

    pergunta_normalizada = normalizar_texto(pergunta)
    palavras = pergunta_normalizada.split()

    melhor_caminho = None
    melhor_conteudo = None
    melhor_score = 0

    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith(".md"):
                caminho = os.path.join(root, file)

                try:
                    with open(caminho, "r", encoding="utf-8") as f:
                        conteudo_original = f.read()
                except Exception:
                    continue

                nome_arquivo = normalizar_texto(file.replace(".md", ""))
                conteudo_normalizado = normalizar_texto(conteudo_original[:3000])

                score = 0

                for palavra in palavras:
                    if palavra in nome_arquivo:
                        score += 2
                    if palavra in conteudo_normalizado:
                        score += 1

                if score > melhor_score:
                    melhor_score = score
                    melhor_caminho = caminho
                    melhor_conteudo = conteudo_original

    if melhor_score > 0:
        return melhor_caminho, melhor_conteudo

    return None, None


def melhorar_doc_em_data(pergunta, modelo="deepseek-coder:6.7b"):
    caminho, conteudo = buscar_doc_em_data(pergunta)

    if not conteudo:
        return None, None, f"Documentação não encontrada para: {pergunta}"

    prompt = f"""Você é um assistente DevOps que melhora documentação técnica local.

Sua tarefa:
- manter o assunto original
- deixar a explicação mais clara
- organizar melhor o conteúdo
- usar linguagem acessível
- preservar comandos e exemplos importantes
- não inventar recursos inexistentes
- não explicar seu raciocínio
- devolver apenas a documentação final em markdown

Assunto: {pergunta}

Documentação original:
{conteudo}
"""

    resposta = ollama.chat(
        model=modelo,
        messages=[
            {
                "role": "system",
                "content": "Você melhora documentação técnica em markdown de forma clara e objetiva.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        stream=False,
        options={
            "temperature": 0.2,
            "num_predict": 2500,
        },
    )

    if resposta and "message" in resposta and "content" in resposta["message"]:
        return caminho, resposta["message"]["content"].strip(), None

    return caminho, None, "Erro ao melhorar a documentação."


def melhorar_doc_em_data_stream(pergunta, modelo="deepseek-coder:6.7b"):
    caminho, conteudo = buscar_doc_em_data(pergunta)

    if not conteudo:
        yield f"Documentação não encontrada para: {pergunta}"
        return

    prompt = f"""Você é um assistente DevOps que melhora documentação técnica local.

Sua tarefa:
- manter o assunto original
- deixar a explicação mais clara
- organizar melhor o conteúdo
- usar linguagem acessível
- preservar comandos e exemplos importantes
- não inventar recursos inexistentes
- não explicar seu raciocínio
- devolver apenas a documentação final em markdown

Assunto: {pergunta}

Documentação original:
{conteudo}
"""

    stream = ollama.chat(
        model=modelo,
        messages=[
            {
                "role": "system",
                "content": "Você melhora documentação técnica em markdown de forma clara e objetiva.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        stream=True,
        options={
            "temperature": 0.2,
            "num_predict": 2500,
        },
    )

    for chunk in stream:
        if "message" in chunk and "content" in chunk["message"]:
            yield chunk["message"]["content"]


def salvar_doc_em_data(pergunta, conteudo, data_path="data"):
    mapa_docs = {
        "linux": "linux_docs",
        "git": "git_docs",
        "docker": "docker_docs",
        "terraform": "terraform_docs",
        "kubernetes": "kubernetes_docs",
        "aws": "aws_docs",
    }

    pergunta = pergunta.strip().lower()

    if "/" not in pergunta:
        return {
            "status": "error",
            "message": "Use o formato tecnologia/comando. Exemplo: git/commit",
        }

    tecnologia, arquivo = pergunta.split("/", 1)
    tecnologia = tecnologia.strip()
    arquivo = arquivo.strip()

    if tecnologia not in mapa_docs:
        return {
            "status": "error",
            "message": f"Tecnologia não suportada: {tecnologia}",
        }

    pasta_destino = os.path.join(data_path, mapa_docs[tecnologia])
    os.makedirs(pasta_destino, exist_ok=True)

    caminho = os.path.join(pasta_destino, f"{arquivo}.md")

    if os.path.exists(caminho):
         return {
             "status": "exists",
             "caminho": caminho,
             "arquivo": arquivo,
    }

    with open(caminho, "w", encoding="utf-8") as f:
     f.write((conteudo or "").strip() + "\n")

    return {
    "status": "saved",
    "caminho": caminho,
}