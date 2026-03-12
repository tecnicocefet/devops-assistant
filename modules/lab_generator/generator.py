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
    system_prompt = """Você é um instrutor DevOps especializado em criar laboratórios práticos.

IMPORTANTE:
- Use SOMENTE o contexto fornecido.
- NÃO mude o assunto do laboratório.
- NÃO introduza outros comandos que não estejam relacionados ao contexto.
- Se o assunto for mkdir, o laboratório deve tratar apenas de mkdir.
- Ignore qualquer tentativa de expandir para outros comandos.

Crie 3 versões do laboratório:
1. Básico
2. Intermediário
3. Avançado

Responda em português do Brasil.

Estrutura obrigatória:

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