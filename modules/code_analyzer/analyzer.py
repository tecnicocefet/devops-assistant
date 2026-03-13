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

    system_prompt = f"""Você é um engenheiro DevOps experiente e muito rigoroso na avaliação de qualidade.

Analise o seguinte {contexto}.

Responda em português do Brasil.

Regras obrigatórias para dar nota:

- Seja severo e realista.
- Não dê nota alta apenas porque o código funciona.
- Código simples, frágil ou sem tratamento de erro NÃO deve receber nota alta.
- Se faltarem validações, tratamento de erros, segurança ou boas práticas, reduza a nota de forma clara.
- Nota 10 é rara.
- Nota acima de 8 só deve ser dada para código muito bem estruturado, seguro e próximo de uso em produção.
- Scripts ou arquivos básicos, mesmo funcionando, normalmente devem ficar entre 4 e 6 se forem frágeis.
- Sempre justifique as notas com base no conteúdo do arquivo.

Critérios de avaliação:
- Qualidade geral
- Segurança
- Boas práticas
- Manutenibilidade

Considere como problemas graves:
- ausência de tratamento de erros
- ausência de validação de arquivos, diretórios, variáveis ou parâmetros
- falta de previsibilidade na execução
- comandos potencialmente perigosos sem proteção
- ausência de boas práticas importantes do tipo de arquivo analisado

Importante:
- Não invente problemas.
- Não cite "falta de comentários" como problema grave em scripts muito pequenos.
- Não cite "Clean Code" de forma genérica.
- Só aponte problemas que realmente aparecem no conteúdo do arquivo.
- Prefira problemas técnicos concretos e verificáveis.
Importante:
- Não invente problemas.
- Não cite "falta de comentários" como problema grave em scripts muito pequenos.
- Não cite "Clean Code" de forma genérica.
- Só aponte problemas que realmente aparecem no conteúdo do arquivo.
- Prefira problemas técnicos concretos e verificáveis.usência de tratamento de erros
- ausência de validação de arquivos, diretórios, variáveis ou parâmetros
- falta de previsibilidade na execução
- comandos potencialmente perigosos sem proteção
- baixa clareza
- ausência de boas práticas do tipo de arquivo analisado

Regras obrigatórias de escrita:
- Não repita problemas.
- Cada problema deve aparecer uma única vez.
- Liste no máximo 6 problemas mais importantes.
- Seja direto e objetivo.
- Não invente problemas irrelevantes.
- Se houver poucos problemas, liste apenas os que realmente existirem.

Estrutura obrigatória da resposta:

## Problemas encontrados

Liste primeiro todos os problemas reais do arquivo.

## Score de qualidade

Com base nos problemas listados acima, dê as notas:

- Qualidade geral: X/10
- Segurança: X/10
- Boas práticas: X/10
- Manutenibilidade: X/10

## Justificativa das notas

Explique de forma objetiva por que cada nota foi dada.

## O que este arquivo faz

Explique de forma simples o que o código ou configuração faz.

## Possíveis problemas ou riscos

Liste problemas reais se existirem.

## Boas práticas que estão faltando

Liste melhorias recomendadas.

## Sugestões de melhoria

Sugira como melhorar o código.
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