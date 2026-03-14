import os
import ollama


LABS_DIR = "labs"


def gerar_lab(assunto, buscar_na_base_fn=None, buscar_doc_em_data_fn=None):
    return {
        "fonte_tipo": "assunto",
        "fonte_caminho": None,
        "conteudo": assunto
    }


def montar_prompt_lab(assunto, contexto, fonte_tipo, fonte_caminho=None):
    system_prompt = """Você é um instrutor DevOps especializado em criar laboratórios práticos de Linux.

Use apenas o assunto e o conteúdo de referência recebidos.
Não altere o assunto do laboratório.
Não invente comandos fora do contexto do assunto.
Não mostre instruções internas.
Não explique como foi gerado o laboratório.
Responda apenas com o laboratório final em português do Brasil.

A resposta deve seguir exatamente esta estrutura:

# LAB: título

## LAB BÁSICO
### Objetivo
### Pré-requisitos
### Cenário
### Passos
### Desafio extra
### Resultado esperado

## LAB INTERMEDIÁRIO
### Objetivo
### Pré-requisitos
### Cenário
### Passos
### Desafio extra
### Resultado esperado

## LAB AVANÇADO
### Objetivo
### Pré-requisitos
### Cenário
### Passos
### Desafio extra
### Resultado esperado

## Fonte
"""

    user_prompt = f"""Assunto do laboratório: {assunto}

Conteúdo de referência:
{contexto}
"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]


def gerar_lab_stream(assunto, modelo):
    if not assunto or not assunto.strip():
        yield "Informe um assunto para gerar o lab. Exemplo: linux/mkdir"
        return

    try:
        resultado_lab = gerar_lab(assunto)

        fonte_tipo = resultado_lab["fonte_tipo"]
        fonte_caminho = resultado_lab["fonte_caminho"]
        contexto = resultado_lab["conteudo"]

        mensagens = montar_prompt_lab(
            assunto=assunto,
            contexto=contexto,
            fonte_tipo=fonte_tipo,
            fonte_caminho=fonte_caminho,
        )

        stream = ollama.chat(
            model=modelo,
            messages=mensagens,
            stream=True,
            options={
                "temperature": 0.2,
                "num_predict": 5000,
            },
        )

        buffer = ""

        for parte in stream:
            texto_parte = parte["message"]["content"]

            if not texto_parte:
                continue

            buffer += texto_parte
            yield texto_parte

        if "## Fonte" not in buffer:
            yield "\n\n⚠️ O laboratório pode ter sido truncado. Tente gerar novamente.\n"

    except Exception as erro:
        yield f"Erro ao gerar lab: {erro}"


def montar_caminho_lab(assunto):
    partes = assunto.split("/", 1)

    if len(partes) == 2:
        tecnologia, nome_lab = partes
        tecnologia = tecnologia.strip().lower()
        nome_lab = nome_lab.strip().lower()
    else:
        tecnologia = "geral"
        nome_lab = assunto.strip().lower().replace(" ", "-")

    pasta_destino = os.path.join(LABS_DIR, tecnologia)
    os.makedirs(pasta_destino, exist_ok=True)

    arquivo_destino = os.path.join(pasta_destino, f"{nome_lab}.md")

    return pasta_destino, arquivo_destino


def montar_caminho_lab_com_nome(assunto, novo_nome):
    partes = assunto.split("/", 1)

    if len(partes) == 2:
        tecnologia, _ = partes
        tecnologia = tecnologia.strip().lower()
    else:
        tecnologia = "geral"

    nome_lab = novo_nome.strip().lower().replace(" ", "-")

    pasta_destino = os.path.join(LABS_DIR, tecnologia)
    os.makedirs(pasta_destino, exist_ok=True)

    arquivo_destino = os.path.join(pasta_destino, f"{nome_lab}.md")

    return pasta_destino, arquivo_destino


def salvar_lab_arquivo(assunto, conteudo_lab, modo="fail", novo_nome=None):
    _, arquivo_destino = montar_caminho_lab(assunto)

    if os.path.exists(arquivo_destino):
        if modo == "fail":
            return {
                "status": "exists",
                "caminho": arquivo_destino
            }

        if modo == "overwrite":
            with open(arquivo_destino, "w", encoding="utf-8") as f:
                f.write(conteudo_lab)

            return {
                "status": "saved",
                "caminho": arquivo_destino,
                "modo": "overwrite"
            }

        if modo == "rename":
            if not novo_nome or not novo_nome.strip():
                return {
                    "status": "error",
                    "message": "novo_nome é obrigatório quando modo='rename'"
                }

            _, novo_arquivo_destino = montar_caminho_lab_com_nome(assunto, novo_nome)

            if os.path.exists(novo_arquivo_destino):
                return {
                    "status": "exists",
                    "caminho": novo_arquivo_destino
                }

            with open(novo_arquivo_destino, "w", encoding="utf-8") as f:
                f.write(conteudo_lab)

            return {
                "status": "saved",
                "caminho": novo_arquivo_destino,
                "modo": "rename"
            }

        return {
            "status": "error",
            "message": f"modo inválido: {modo}"
        }

    with open(arquivo_destino, "w", encoding="utf-8") as f:
        f.write(conteudo_lab)

    return {
        "status": "saved",
        "caminho": arquivo_destino,
        "modo": "new"
    }

def listar_labs_salvos():
    labs = []

    if not os.path.exists(LABS_DIR):
        return labs

    for tecnologia in sorted(os.listdir(LABS_DIR)):
        pasta_tecnologia = os.path.join(LABS_DIR, tecnologia)

        if not os.path.isdir(pasta_tecnologia):
            continue

        for arquivo in sorted(os.listdir(pasta_tecnologia)):
            if not arquivo.endswith(".md"):
                continue

            caminho_arquivo = os.path.join(pasta_tecnologia, arquivo)

            labs.append({
                "tecnologia": tecnologia,
                "arquivo": arquivo,
                "caminho": caminho_arquivo,
                "nome": arquivo[:-3]
            })

    return labs

def ler_lab_salvo(tecnologia, nome):
    arquivo_destino = os.path.join(LABS_DIR, tecnologia, f"{nome}.md")

    if not os.path.exists(arquivo_destino):
        return {
            "status": "error",
            "message": "Lab não encontrado."
        }

    with open(arquivo_destino, "r", encoding="utf-8") as f:
        conteudo = f.read()

    return {
        "status": "ok",
        "tecnologia": tecnologia,
        "nome": nome,
        "caminho": arquivo_destino,
        "conteudo": conteudo
    }