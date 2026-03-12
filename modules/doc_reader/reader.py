import os
import re


def ler_arquivo(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()

    return conteudo


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
        "aws": "aws_docs"
    }

    pergunta = pergunta.strip().lower()

    if "/" in pergunta:
        try:
            tecnologia, arquivo = pergunta.split("/", 1)
            tecnologia = tecnologia.strip()
            arquivo = arquivo.strip()

            if tecnologia in mapa_docs:
                caminho = os.path.join(data_path, mapa_docs[tecnologia], f"{arquivo}.md")

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