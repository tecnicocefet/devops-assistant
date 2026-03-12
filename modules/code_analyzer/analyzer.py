import os


def detectar_tipo_arquivo(caminho):
    nome = caminho.lower()

    if nome.endswith(".sh"):
        return "bash"

    if "dockerfile" in nome:
        return "docker"

    if nome.endswith(".yaml") or nome.endswith(".yml"):
        return "yaml"

    if nome.endswith(".tf"):
        return "terraform"

    if nome.endswith(".conf"):
        return "config"

    return "generic"


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
    tipo = detectar_tipo_arquivo(caminho)

    if tipo == "bash":
        contexto = "script Bash"
    elif tipo == "docker":
        contexto = "Dockerfile"
    elif tipo == "yaml":
        contexto = "arquivo YAML possivelmente usado em Kubernetes ou configuração"
    elif tipo == "terraform":
        contexto = "código Terraform (Infrastructure as Code)"
    elif tipo == "config":
        contexto = "arquivo de configuração de serviço"
    else:
        contexto = "arquivo de código ou configuração"

    system_prompt = f"""Você é um engenheiro DevOps experiente.

Analise o seguinte {contexto}.

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


def montar_prompt_correcao(caminho, conteudo):
    tipo = detectar_tipo_arquivo(caminho)

    if tipo == "bash":
        contexto = "script Bash"
    elif tipo == "docker":
        contexto = "Dockerfile"
    elif tipo == "yaml":
        contexto = "arquivo YAML possivelmente usado em Kubernetes"
    elif tipo == "terraform":
        contexto = "código Terraform"
    elif tipo == "config":
        contexto = "arquivo de configuração"
    else:
        contexto = "arquivo de código ou configuração"

    system_prompt = f"""Você é um engenheiro DevOps experiente.

Receberá um {contexto} que pode ter problemas.

Sua tarefa:

1. Identificar problemas
2. Corrigir o código
3. Gerar uma versão melhorada

Responda no formato:

## Problemas encontrados

## Código corrigido

Use blocos de código.
Responda em português do Brasil.
"""

    user_prompt = f"""
Arquivo: {caminho}

Conteúdo original:

{conteudo}
"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]