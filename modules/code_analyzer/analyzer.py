import os
import shutil
import subprocess
import tempfile

import ollama


def detectar_tipo_arquivo(caminho):
    nome = (caminho or "").strip().lower()

    if nome == "dockerfile" or nome.endswith("/dockerfile") or nome.endswith("\\dockerfile"):
        return "docker"

    if "docker-compose" in nome or nome.endswith("compose.yaml") or nome.endswith("compose.yml"):
        return "compose"

    if nome.endswith(".yaml") or nome.endswith(".yml"):
        return "yaml"

    if nome.endswith(".sh"):
        return "bash"

    if nome.endswith(".tf"):
        return "terraform"

    if nome.endswith(".conf"):
        return "config"

    return "generic"


def detectar_tipo_por_conteudo(conteudo):
    texto = (conteudo or "").strip()

    if not texto:
        return "generic"

    texto_lower = texto.lower()
    linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
    primeiras_linhas = "\n".join(linhas[:12]).lower()

    if texto.startswith("#!/bin/bash") or texto.startswith("#!/usr/bin/env bash"):
        return "bash"

    if any(token in primeiras_linhas for token in ["if [", "then", "fi", "mkdir ", "cp ", "echo "]):
        return "bash"

    if any(
        linha.lower().startswith(
            ("from ", "run ", "copy ", "cmd ", "entrypoint ", "workdir ", "expose ")
        )
        for linha in linhas[:12]
    ):
        return "docker"

    if any(
        token in texto_lower
        for token in ['resource "', 'provider "', 'variable "', 'output "', 'terraform {']
    ):
        return "terraform"

    if "services:" in texto_lower and any(
        token in texto_lower for token in ["image:", "ports:", "volumes:", "environment:", "build:"]
    ):
        return "compose"

    if ":" in texto and ("\n-" in texto or "\n  " in texto):
        return "yaml"

    return "generic"


def ler_codigo(caminho):
    if not os.path.exists(caminho):
        return None, "Arquivo não encontrado."

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo = f.read()
    except Exception as exc:
        return None, f"Erro ao ler arquivo: {exc}"

    return conteudo, None


def _bloco_linguagem(tipo):
    if tipo == "bash":
        return "bash"
    if tipo == "docker":
        return "dockerfile"
    if tipo in ("yaml", "compose"):
        return "yaml"
    if tipo == "terraform":
        return "hcl"
    if tipo == "config":
        return "conf"
    return "text"


def _executar_comando(comando, cwd=None):
    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            cwd=cwd,
        )
        return resultado.returncode, (resultado.stdout or "").strip(), (resultado.stderr or "").strip()
    except Exception as exc:
        return 1, "", str(exc)


def _juntar_saida(stdout, stderr):
    return "\n".join([parte for parte in [stdout, stderr] if parte]).strip()


def _resultado_ok(fonte):
    return {
        "ok": True,
        "fonte": fonte,
        "itens": [],
    }


def _resultado_erro(fonte, saida):
    itens = [linha for linha in (saida or "").splitlines() if linha.strip()]

    if not itens:
        itens = [f"{fonte} retornou erro, mas sem detalhes."]

    return {
        "ok": False,
        "fonte": fonte,
        "itens": itens,
    }


def _agrupar_resultados(resultados):
    resultados_validos = [r for r in resultados if r is not None]

    if not resultados_validos:
        return None

    erros = []
    fontes = []

    for resultado in resultados_validos:
        fonte = resultado.get("fonte")
        if fonte and fonte not in fontes:
            fontes.append(fonte)

        if not resultado.get("ok", False):
            erros.extend(resultado.get("itens", []))

    if erros:
        return {
            "ok": False,
            "fonte": " + ".join(fontes),
            "itens": erros,
        }

    return {
        "ok": True,
        "fonte": " + ".join(fontes),
        "itens": [],
    }


def _validar_bash(nome_arquivo, conteudo):
    resultados = []

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".sh",
        delete=False,
        encoding="utf-8",
    ) as tmp:
        tmp.write(conteudo)
        caminho_tmp = tmp.name

    try:
        if shutil.which("shellcheck"):
            rc, stdout, stderr = _executar_comando(["shellcheck", "-f", "gcc", caminho_tmp])
            saida = _juntar_saida(stdout, stderr)

            if rc == 0:
                resultados.append(_resultado_ok("shellcheck"))
            else:
                resultados.append(_resultado_erro("shellcheck", saida))

        if shutil.which("bash"):
            rc, stdout, stderr = _executar_comando(["bash", "-n", caminho_tmp])
            saida = _juntar_saida(stdout, stderr)

            if rc == 0:
                resultados.append(_resultado_ok("bash -n"))
            else:
                resultados.append(_resultado_erro("bash -n", saida))

        if shutil.which("shfmt"):
            rc, stdout, stderr = _executar_comando(["shfmt", "-d", caminho_tmp])
            saida = _juntar_saida(stdout, stderr)

            if rc == 0:
                resultados.append(_resultado_ok("shfmt -d"))
            else:
                resultados.append(_resultado_erro("shfmt -d", saida))

        return _agrupar_resultados(resultados)

    finally:
        try:
            os.remove(caminho_tmp)
        except OSError:
            pass


def _validar_yaml(nome_arquivo, conteudo):
    sufixo = ".yml" if nome_arquivo.lower().endswith(".yml") else ".yaml"

    if not shutil.which("yamllint"):
        return None

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=sufixo,
        delete=False,
        encoding="utf-8",
    ) as tmp:
        tmp.write(conteudo)
        caminho_tmp = tmp.name

    try:
        rc, stdout, stderr = _executar_comando(["yamllint", "-f", "parsable", caminho_tmp])
        saida = _juntar_saida(stdout, stderr)

        if rc == 0:
            return _resultado_ok("yamllint")

        return _resultado_erro("yamllint", saida)
    finally:
        try:
            os.remove(caminho_tmp)
        except OSError:
            pass


def _validar_docker(nome_arquivo, conteudo):
    if not shutil.which("hadolint"):
        return None

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".Dockerfile",
        delete=False,
        encoding="utf-8",
    ) as tmp:
        tmp.write(conteudo)
        caminho_tmp = tmp.name

    try:
        rc, stdout, stderr = _executar_comando(["hadolint", caminho_tmp])
        saida = _juntar_saida(stdout, stderr)

        if rc == 0:
            return _resultado_ok("hadolint")

        return _resultado_erro("hadolint", saida)
    finally:
        try:
            os.remove(caminho_tmp)
        except OSError:
            pass


def _validar_compose(nome_arquivo, conteudo):
    resultados = []

    with tempfile.TemporaryDirectory() as tmpdir:
        caminho_tmp = os.path.join(tmpdir, "docker-compose.yml")

        with open(caminho_tmp, "w", encoding="utf-8") as f:
            f.write(conteudo)

        if shutil.which("docker"):
            rc, stdout, stderr = _executar_comando(
                ["docker", "compose", "-f", caminho_tmp, "config"],
                cwd=tmpdir,
            )
            saida = _juntar_saida(stdout, stderr)

            if rc == 0:
                resultados.append(_resultado_ok("docker compose config"))
            else:
                resultados.append(_resultado_erro("docker compose config", saida))

        yaml_resultado = _validar_yaml(nome_arquivo, conteudo)
        if yaml_resultado is not None:
            resultados.append(yaml_resultado)

    return _agrupar_resultados(resultados)


def _validar_terraform(nome_arquivo, conteudo):
    if not shutil.which("terraform"):
        return None

    resultados = []

    with tempfile.TemporaryDirectory() as tmpdir:
        caminho_tmp = os.path.join(tmpdir, "main.tf")

        with open(caminho_tmp, "w", encoding="utf-8") as f:
            f.write(conteudo)

        rc, stdout, stderr = _executar_comando(
            ["terraform", "fmt", "-check", "-diff", "-no-color", caminho_tmp],
            cwd=tmpdir,
        )
        saida = _juntar_saida(stdout, stderr)

        if rc == 0:
            resultados.append(_resultado_ok("terraform fmt -check"))
        else:
            resultados.append(_resultado_erro("terraform fmt -check", saida))

        rc, stdout, stderr = _executar_comando(
            ["terraform", "init", "-backend=false", "-input=false", "-no-color"],
            cwd=tmpdir,
        )

        if rc == 0:
            rc, stdout, stderr = _executar_comando(
                ["terraform", "validate", "-no-color"],
                cwd=tmpdir,
            )
            saida = _juntar_saida(stdout, stderr)

            if rc == 0:
                resultados.append(_resultado_ok("terraform validate"))
            else:
                resultados.append(_resultado_erro("terraform validate", saida))
        else:
            saida = _juntar_saida(stdout, stderr)
            resultados.append(_resultado_erro("terraform init", saida))

    return _agrupar_resultados(resultados)


def validar_codigo(nome_arquivo, conteudo):
    tipo = detectar_tipo_arquivo(nome_arquivo)

    if tipo == "generic":
        tipo = detectar_tipo_por_conteudo(conteudo)

    print("DEBUG tipo =", tipo)

    if tipo == "bash":
        return _validar_bash(nome_arquivo, conteudo)

    if tipo == "yaml":
        return _validar_yaml(nome_arquivo, conteudo)

    if tipo == "docker":
        return _validar_docker(nome_arquivo, conteudo)

    if tipo == "compose":
        return _validar_compose(nome_arquivo, conteudo)

    if tipo == "terraform":
        return _validar_terraform(nome_arquivo, conteudo)

    return None


def montar_prompt_analise_texto(nome_arquivo, conteudo):
    tipo = detectar_tipo_arquivo(nome_arquivo)

    if tipo == "generic":
        tipo = detectar_tipo_por_conteudo(conteudo)

    linguagem = _bloco_linguagem(tipo)

    prompt = (
        "Você é um assistente técnico de DevOps.\n\n"
        "Analise o código abaixo e responda de forma clara para um estudante iniciante.\n\n"
        "Regras:\n"
        "1. Explique o que o código faz.\n"
        "2. Aponte problemas ou melhorias importantes.\n"
        "3. Se fizer sentido, mostre uma versão melhorada.\n"
        "4. Seja direto e didático.\n"
        "5. Responda em português.\n\n"
        "Formato:\n\n"
        "## Diagnóstico\n\n"
        "<explicação>\n\n"
        "## Sugestão\n\n"
        f"```{linguagem}\n"
        "<se houver sugestão de melhoria>\n"
        "```\n\n"
        f"Tipo detectado: {tipo}\n"
        f"Nome do arquivo: {nome_arquivo}\n\n"
        f"Código:\n```{linguagem}\n{conteudo}\n```"
    )

    return [{"role": "user", "content": prompt}]
def montar_prompt_analise(nome_arquivo, conteudo):
    return montar_prompt_analise_texto(nome_arquivo, conteudo)

def montar_prompt_correcao(nome_arquivo, conteudo):
    tipo = detectar_tipo_arquivo(nome_arquivo)

    if tipo == "generic":
        tipo = detectar_tipo_por_conteudo(conteudo)

    linguagem = _bloco_linguagem(tipo)

    prompt = (
        "Você é um assistente técnico de DevOps.\n\n"
        "Corrija o código abaixo.\n\n"
        "Regras:\n"
        "1. Explique brevemente os problemas encontrados.\n"
        "2. Mostre o código corrigido completo.\n"
        "3. Preserve ao máximo a intenção original do código.\n"
        "4. Responda em português.\n"
        "5. Não invente ferramentas ou contextos que não aparecem no código.\n\n"
        "Formato:\n\n"
        "## Diagnóstico\n\n"
        "<explicação curta>\n\n"
        "## Código corrigido\n\n"
        f"```{linguagem}\n"
        "<CÓDIGO CORRIGIDO COMPLETO>\n"
        "```\n\n"
        f"Tipo detectado: {tipo}\n"
        f"Nome do arquivo: {nome_arquivo}\n\n"
        f"Código original:\n```{linguagem}\n{conteudo}\n```"
    )

    return [{"role": "user", "content": prompt}]


def _montar_resposta_validacao(modelo, nome_arquivo, conteudo, resultado_validacao):
    tipo = detectar_tipo_arquivo(nome_arquivo)

    if tipo == "generic":
        tipo = detectar_tipo_por_conteudo(conteudo)

    linguagem = _bloco_linguagem(tipo)

    if resultado_validacao["ok"]:
        return (
            "## Diagnóstico\n\n"
            "O código passou na validação real.\n\n"
            "## Código\n\n"
            f"```{linguagem}\n{conteudo}\n```"
        )

    erros_reais = "\n".join(resultado_validacao.get("itens", []))

    prompt = (
        "Você é um assistente técnico de DevOps.\n\n"
        "O validator real encontrou erros no código.\n"
        "Sua tarefa é explicar esses erros em linguagem simples e mostrar o código corrigido completo.\n\n"
        "Regras obrigatórias:\n"
        "1. Explique em linguagem simples, para estudante iniciante.\n"
        "2. NÃO mostre caminhos temporários, códigos internos ou mensagens cruas do validator.\n"
        "3. NÃO mencione códigos como SC2154, caminhos /tmp, linha ou coluna.\n"
        "4. Mostre o código corrigido COMPLETO.\n"
        "5. NÃO repita o código original sem corrigir.\n"
        "6. Preserve ao máximo a intenção original do código.\n"
        "7. Responda em português.\n"
        "8. Responda exatamente neste formato:\n\n"
        "## Diagnóstico\n\n"
        "<explicação simples e curta>\n\n"
        "## Código corrigido\n\n"
        f"```{linguagem}\n"
        "<CÓDIGO COMPLETO CORRIGIDO>\n"
        "```\n\n"
        f"Tipo detectado: {tipo}\n"
        f"Validator usado: {resultado_validacao['fonte']}\n\n"
        f"Erros reais do validator:\n{erros_reais}\n\n"
        f"Código original:\n```{linguagem}\n{conteudo}\n```"
    )

    partes = []

    stream = ollama.chat(
        model=modelo,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        options={
            "temperature": 0.1,
            "num_predict": 1200,
        },
    )

    for chunk in stream:
        if "message" in chunk and "content" in chunk["message"]:
            texto = chunk["message"]["content"]
            if texto:
                partes.append(texto)

    resposta = "".join(partes).strip()

    if not resposta:
        return (
            "## Diagnóstico\n\n"
            "Encontrei erros no código, mas não consegui gerar a correção automática.\n\n"
            "## Código corrigido\n\n"
            "Não foi possível gerar a correção nesta etapa.\n"
        )

    return resposta


def analisar_texto(modelo, nome_arquivo, conteudo):
    if not conteudo or not conteudo.strip():
        return None, "Conteúdo vazio."

    try:
        resultado_validacao = validar_codigo(nome_arquivo, conteudo)

        if resultado_validacao is not None:
            resposta = _montar_resposta_validacao(
                modelo,
                nome_arquivo,
                conteudo,
                resultado_validacao,
            )
            return resposta, None

        mensagens = montar_prompt_analise_texto(nome_arquivo, conteudo)

        resposta = ollama.chat(
            model=modelo,
            messages=mensagens,
            options={
                "temperature": 0.1,
                "num_predict": 1200,
                "stop": [
                    "### Instruction:",
                    "### Response:",
                    "Instruction:",
                    "Response:",
                    "User:",
                    "Assistant:",
                ],
            },
        )

        return resposta["message"]["content"], None

    except Exception as exc:
        return None, f"Erro ao analisar conteúdo: {exc}"


def analisar_texto_stream(modelo, nome_arquivo, conteudo):
    if not conteudo or not conteudo.strip():
        yield "Conteúdo vazio.\n"
        return

    try:
        resultado_validacao = validar_codigo(nome_arquivo, conteudo)
        print("DEBUG resultado_validacao =", resultado_validacao)

        if resultado_validacao is not None:
            resposta_validacao = _montar_resposta_validacao(
                modelo,
                nome_arquivo,
                conteudo,
                resultado_validacao,
            )

            if not resposta_validacao:
                resposta_validacao = "Erro ao montar resposta da validação."

            print("DEBUG entrou no return da validacao")
            print("DEBUG resposta_validacao =", repr(resposta_validacao))

            yield resposta_validacao + "\n"
            return

        mensagens = montar_prompt_analise_texto(nome_arquivo, conteudo)

        stream = ollama.chat(
            model=modelo,
            messages=mensagens,
            stream=True,
            options={
                "temperature": 0.1,
                "num_predict": 1200,
                "stop": [
                    "### Instruction:",
                    "### Response:",
                    "Instruction:",
                    "Response:",
                    "User:",
                    "Assistant:",
                ],
            },
        )

        for chunk in stream:
            if "message" in chunk and "content" in chunk["message"]:
                texto = chunk["message"]["content"]
                if texto:
                    yield texto

    except Exception as exc:
        yield f"Erro ao analisar conteúdo: {exc}\n"


def corrigir_texto_stream(modelo, nome_arquivo, conteudo):
    if not conteudo or not conteudo.strip():
        yield "Conteúdo vazio."
        return

    try:
        resultado_validacao = validar_codigo(nome_arquivo, conteudo)

        if resultado_validacao is not None and resultado_validacao["ok"]:
            tipo = detectar_tipo_arquivo(nome_arquivo)

            if tipo == "generic":
                tipo = detectar_tipo_por_conteudo(conteudo)

            linguagem = _bloco_linguagem(tipo)

            yield "## Diagnóstico\n\n"
            yield "O código já passou na validação real.\n\n"
            yield "## Código corrigido\n\n"
            yield f"```{linguagem}\n{conteudo}\n```"
            return

        if resultado_validacao is not None and not resultado_validacao["ok"]:
            resposta_validacao = _montar_resposta_validacao(
                modelo,
                nome_arquivo,
                conteudo,
                resultado_validacao,
            )
            yield resposta_validacao
            return

        mensagens = montar_prompt_correcao(nome_arquivo, conteudo)

        stream = ollama.chat(
            model=modelo,
            messages=mensagens,
            stream=True,
            options={
                "temperature": 0.1,
                "num_predict": 900,
                "stop": [
                    "### Instruction:",
                    "### Response:",
                    "Instruction:",
                    "Response:",
                    "User:",
                    "Assistant:",
                ],
            },
        )

        for chunk in stream:
            if "message" in chunk and "content" in chunk["message"]:
                texto = chunk["message"]["content"]
                if texto:
                    yield texto

    except Exception as exc:
        yield f"Erro ao corrigir conteúdo: {exc}"