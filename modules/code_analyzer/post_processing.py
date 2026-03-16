import re


def _normalizar_texto(texto: str) -> str:
    texto = texto.lower().strip()
    texto = re.sub(r"^\d+[\).\-\s]+", "", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto


def remover_itens_duplicados(texto: str) -> str:
    linhas = texto.splitlines()
    novas_linhas = []
    vistos = set()

    for linha in linhas:
        linha_strip = linha.strip()

        if re.match(r"^\d+[\).\-\s]+", linha_strip) or linha_strip.startswith("- "):
            chave = _normalizar_texto(linha_strip)
            if chave in vistos:
                continue
            vistos.add(chave)

        novas_linhas.append(linha)

    return "\n".join(novas_linhas)
