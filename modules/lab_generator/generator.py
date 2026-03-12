def gerar_lab(assunto, buscar_na_base_fn, buscar_doc_em_data_fn):
    caminho_base, conteudo_base = buscar_na_base_fn(assunto)

    if caminho_base and conteudo_base:
        return {
            "fonte_tipo": "knowledge-base",
            "fonte_caminho": caminho_base,
            "conteudo": conteudo_base
        }

    caminho_doc, conteudo_doc = buscar_doc_em_data_fn(assunto)

    if caminho_doc and conteudo_doc:
        return {
            "fonte_tipo": "data",
            "fonte_caminho": caminho_doc,
            "conteudo": conteudo_doc
        }

    return {
        "fonte_tipo": "assunto",
        "fonte_caminho": None,
        "conteudo": assunto
    }


def montar_prompt_lab(assunto, contexto, fonte_tipo, fonte_caminho=None):
    system_prompt = """Você é um instrutor DevOps especializado em criar laboratórios práticos para estudo.

Crie um lab prático, didático e progressivo.

REGRAS:
- Responda em português do Brasil.
- Use linguagem clara e objetiva.
- O lab deve ser voltado para estudo prático.
- Não invente tecnologias fora do contexto.
- Sempre organize a resposta com os títulos abaixo.
- Se o contexto for pequeno, complete com um exercício simples e coerente.
- Priorize exercícios que possam ser executados localmente quando possível.

Estrutura obrigatória:

# LAB: título do laboratório

## Objetivo

## Pré-requisitos

## Cenário

## Passos

## Desafio extra

## Resultado esperado
"""

    user_prompt = f"""
Assunto: {assunto}

Tipo de fonte: {fonte_tipo}

Caminho da fonte: {fonte_caminho if fonte_caminho else "não informado"}

Contexto:
{contexto}
"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]