import subprocess
import shutil
import re
import os
import ollama


def limpar_man_page(texto):
    # remove marcações com backspace usadas em algumas man pages
    texto = re.sub(r".\x08", "", texto)

    # remove excesso de linhas vazias seguidas
    linhas = texto.splitlines()
    linhas_limpas = []
    linha_vazia_anterior = False

    for linha in linhas:
        linha = linha.rstrip()
        linha_vazia = not linha.strip()

        if linha_vazia and linha_vazia_anterior:
            continue

        linhas_limpas.append(linha)
        linha_vazia_anterior = linha_vazia

    return "\n".join(linhas_limpas).strip()


def ler_man_page(comando):
    comando = comando.strip()

    if not comando:
        return None, "Informe um comando. Exemplo: mkdir"

    if shutil.which("man") is None:
        return None, "O comando 'man' não está instalado no sistema."

    try:
        resultado = subprocess.run(
            ["man", comando],
            capture_output=True,
            text=True,
            env={"MANPAGER": "cat", "PAGER": "cat", "LANG": "C", "LC_ALL": "C"},
        )

        if resultado.returncode != 0:
            erro = (resultado.stderr or "").strip()

            if erro:
                return None, f"Erro ao consultar man page de '{comando}': {erro}"

            return None, f"Man page não encontrada para: {comando}"

        conteudo = resultado.stdout.strip()

        if not conteudo:
            return None, f"A man page de '{comando}' veio vazia."

        conteudo = limpar_man_page(conteudo)

        # limitar tamanho para não mandar a man page inteira para o modelo
        conteudo = conteudo[:4000]

        return conteudo, None

    except Exception as erro:
        return None, f"Erro ao executar man: {erro}"


def explicar_man_page(comando, modelo="deepseek-coder:6.7b"):
    conteudo, erro = ler_man_page(comando)

    if erro:
        return None, erro

    prompt = f"""Explique este comando Linux de forma clara e didática.

Organize a resposta em markdown com:

# Comando
# O que ele faz
# Opções importantes
# Exemplos práticos

Comando: {comando}

Conteúdo da man page:
{conteudo}
"""

    resposta = ollama.chat(
        model=modelo,
        messages=[
            {
                "role": "system",
                "content": "Você explica comandos Linux de forma clara e didática.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        stream=False,
        options={
            "temperature": 0.2,
            "num_predict": 2000,
        },
    )

    texto = resposta["message"]["content"].strip()

    return texto, None


def salvar_man_como_doc(comando, conteudo, data_path="data"):
    comando = comando.strip().lower()

    if not comando:
        return {
            "status": "error",
            "message": "Informe um comando para salvar.",
        }

    pasta_destino = os.path.join(data_path, "linux_docs")
    os.makedirs(pasta_destino, exist_ok=True)

    caminho = os.path.join(pasta_destino, f"{comando}.md")

    with open(caminho, "w", encoding="utf-8") as f:
        f.write((conteudo or "").strip() + "\n")

    return {
        "status": "saved",
        "caminho": caminho,
    }
