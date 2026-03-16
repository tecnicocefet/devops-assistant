import math
import re


def _contar_linhas_reais(conteudo: str) -> int:
    linhas = [linha for linha in conteudo.splitlines() if linha.strip()]
    return len(linhas)


def _eh_script_pequeno(conteudo: str) -> bool:
    return _contar_linhas_reais(conteudo) < 10


def _normalizar_score(valor: float) -> int:
    valor = max(0, min(10, round(valor)))
    return int(valor)


def _contar_ocorrencias_texto(texto: str, termos: list[str]) -> int:
    texto_lower = texto.lower()
    total = 0
    for termo in termos:
        total += texto_lower.count(termo.lower())
    return total


def _extrair_qtd_problemas_validacao(resultado_validacao) -> int:
    if not resultado_validacao:
        return 0

    if isinstance(resultado_validacao, str):
        texto = resultado_validacao.strip()
        if not texto:
            return 0
        return len([linha for linha in texto.splitlines() if linha.strip()])

    if isinstance(resultado_validacao, dict):
        total = 0
        for valor in resultado_validacao.values():
            if isinstance(valor, str):
                total += len([linha for linha in valor.splitlines() if linha.strip()])
            elif isinstance(valor, list):
                total += len(valor)
        return total

    return 1


def calcular_scores_arquivo(
    nome_arquivo: str,
    conteudo: str,
    resultado_validacao=None,
    problemas_confirmados: list[str] | None = None,
) -> dict:
    problemas_confirmados = problemas_confirmados or []

    linhas = _contar_linhas_reais(conteudo)
    pequeno = _eh_script_pequeno(conteudo)
    qtd_validacoes = _extrair_qtd_problemas_validacao(resultado_validacao)
    qtd_problemas = len(problemas_confirmados)

    # Base proporcional ao tamanho / complexidade
    if pequeno:
        base_qualidade = 8.0
        base_seguranca = 8.0
        base_boas_praticas = 7.0
        base_manutenibilidade = 8.0
    elif linhas <= 50:
        base_qualidade = 7.0
        base_seguranca = 7.0
        base_boas_praticas = 7.0
        base_manutenibilidade = 7.0
    else:
        base_qualidade = 6.5
        base_seguranca = 6.5
        base_boas_praticas = 6.5
        base_manutenibilidade = 6.5

    penalidade_validacao = min(4.0, qtd_validacoes * 0.8)
    penalidade_problemas = min(3.0, qtd_problemas * 0.5)

    texto = conteudo.lower()

    penalidade_seguranca_extra = 0.0
    penalidade_boas_praticas_extra = 0.0
    penalidade_manutenibilidade_extra = 0.0

    if "rm -rf" in texto:
        penalidade_seguranca_extra += 2.0

    if re.search(r"\bcurl\b.*\|\s*(bash|sh)\b", texto):
        penalidade_seguranca_extra += 2.0

    if "chmod 777" in texto:
        penalidade_seguranca_extra += 1.5

    if pequeno and not resultado_validacao:
        # script pequeno e sem erro real não deve despencar nota
        penalidade_problemas *= 0.5

    if _contar_ocorrencias_texto(texto, ["TODO", "FIXME"]) > 0:
        penalidade_manutenibilidade_extra += 0.5

    if linhas > 30 and "#" not in conteudo:
        penalidade_manutenibilidade_extra += 0.5

    if pequeno:
        penalidade_manutenibilidade_extra = min(penalidade_manutenibilidade_extra, 0.5)

    qualidade = base_qualidade - penalidade_validacao - penalidade_problemas
    seguranca = base_seguranca - penalidade_validacao - penalidade_seguranca_extra
    boas_praticas = (
        base_boas_praticas
        - (penalidade_problemas * 0.8)
        - (penalidade_validacao * 0.6)
        - penalidade_boas_praticas_extra
    )
    manutenibilidade = (
        base_manutenibilidade - penalidade_problemas - penalidade_manutenibilidade_extra
    )

    return {
        "qualidade_geral": _normalizar_score(qualidade),
        "seguranca": _normalizar_score(seguranca),
        "boas_praticas": _normalizar_score(boas_praticas),
        "manutenibilidade": _normalizar_score(manutenibilidade),
        "linhas_reais": linhas,
        "script_pequeno": pequeno,
        "qtd_problemas_confirmados": qtd_problemas,
        "qtd_problemas_validacao": qtd_validacoes,
    }
