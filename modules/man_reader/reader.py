import subprocess
import shutil
import re


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
        return None, "Informe um comando. Exemplo: man:mkdir"

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
        conteudo = conteudo[:1200]

        return conteudo, None

    except Exception as erro:
        return None, f"Erro ao executar man: {erro}"
