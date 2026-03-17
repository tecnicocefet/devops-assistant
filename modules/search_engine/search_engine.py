import os

PASTAS_BUSCA_PADRAO = [
    "data",
    "knowledge-base",
]


def _eh_arquivo_texto(caminho):
    extensoes_validas = {
        ".md",
        ".txt",
        ".sh",
        ".yaml",
        ".yml",
        ".tf",
        ".conf",
        ".json",
        ".log",
    }

    _, ext = os.path.splitext(caminho.lower())
    return ext in extensoes_validas


def _listar_arquivos(base_dirs=None):
    base_dirs = base_dirs or PASTAS_BUSCA_PADRAO
    arquivos = []

    for pasta in base_dirs:
        if not os.path.exists(pasta):
            continue

        for raiz, _, nomes in os.walk(pasta):
            for nome in nomes:
                caminho = os.path.join(raiz, nome)

                if _eh_arquivo_texto(caminho):
                    arquivos.append(caminho)

    return arquivos


def _ler_arquivo(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


def _extrair_trecho(conteudo, termo, contexto=3):
    linhas = conteudo.splitlines()
    termo_lower = termo.lower()

    for i, linha in enumerate(linhas):
        if termo_lower in linha.lower():
            inicio = max(0, i - contexto)
            fim = min(len(linhas), i + contexto + 1)

            trecho = linhas[inicio:fim]

            # remover blocos markdown ``` para não poluir
            trecho = [l for l in trecho if not l.strip().startswith("```")]

            # remover linhas vazias no começo/fim
            while trecho and not trecho[0].strip():
                trecho.pop(0)

            while trecho and not trecho[-1].strip():
                trecho.pop()

            return "\n".join(trecho)

    return ""


def buscar_na_base_local(termo, base_dirs=None, limite=10):
    termo = (termo or "").strip()

    if not termo:
        return []

    resultados = []
    termo_lower = termo.lower()

    for caminho in _listar_arquivos(base_dirs):
        nome_arquivo = os.path.basename(caminho).lower()

        conteudo = _ler_arquivo(caminho)
        if conteudo is None:
            continue

        conteudo_lower = conteudo.lower()
        linhas = conteudo.splitlines()

        score = 0
        trecho = ""

        if termo_lower in nome_arquivo:
            score += 5

        ocorrencias = conteudo_lower.count(termo_lower)
        if ocorrencias > 0:
            score += min(10, ocorrencias * 2)
            trecho = _extrair_trecho(conteudo, termo)

        for linha in linhas[:8]:
            linha_lower = linha.strip().lower()

            if linha_lower.startswith("#") and termo_lower in linha_lower:
                score += 4

            if linha_lower.startswith("comando:") and termo_lower in linha_lower:
                score += 3

        inicio_conteudo = "\n".join(linhas[:15]).lower()
        if termo_lower in inicio_conteudo:
            score += 2

        if score > 0:
            resultados.append(
                {
                    "caminho": caminho,
                    "score": score,
                    "trecho": trecho,
                }
            )

    resultados.sort(key=lambda x: (-x["score"], x["caminho"]))

    return resultados[:limite]
