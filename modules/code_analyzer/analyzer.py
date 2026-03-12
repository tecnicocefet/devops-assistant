import os


def ler_codigo(caminho):
    if not os.path.exists(caminho):
        return None, "Arquivo não encontrado."

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception as e:
        return None, f"Erro ao ler arquivo: {e}"

    return conteudo, None


def montar_prompt_analise(caminho, conteudo):
    system_prompt = """Você é um engenheiro DevOps experiente.

Analise o arquivo fornecido.

Explique de forma clara:

1. O que este código ou configuração faz
2. Possíveis problemas ou riscos
3. Boas práticas que estão faltando
4. Sugestões de melhoria

Responda em português do Brasil.
"""

    user_prompt = f"""
Arquivo analisado: {caminho}

Conteúdo do arquivo:

{conteudo}
"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]