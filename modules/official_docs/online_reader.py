import subprocess
import requests
from bs4 import BeautifulSoup


def limpar_linhas(texto):
    linhas = []

    ignorar = {
        "English",
        "Deutsch",
        "Español",
        "Français",
        "Íslenska",
        "日本語",
        "Português (Brasil)",
        "Română",
        "Русский",
        "Svenska",
        "українська мова",
        "简体中文",
        "Topics",
    }

    for linha in texto.splitlines():
        linha = linha.strip()

        if not linha:
            continue

        if linha in ignorar:
            continue

        if len(linha) < 2:
            continue

        linhas.append(linha)

    return linhas


def remover_lixo_modelo(texto):
    lixo = [
        "<｜begin▁of▁sentence｜>",
        "Expected output:",
        "def main():",
        "Obrigado por ler até aqui",
        'digite "-1"',
        'digite "0"',
        "python",
        "main()",
        "Ao invés de",
        "Como fazer isto",
        "forçar o Git",
        "```",
        '"""',
    ]

    linhas_filtradas = []

    for linha in texto.splitlines():
        linha = linha.strip()

        if not linha:
            continue

        if any(item.lower() in linha.lower() for item in lixo):
            continue

        if linha in {"{", "}", "```"}:
            continue

        linhas_filtradas.append(linha)

    return "\n".join(linhas_filtradas)


def extrair_texto_generico(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()

    main = (
        soup.find("main")
        or soup.find("article")
        or soup.find("div", class_="body")
        or soup.find("div", class_="content")
        or soup
    )

    texto = main.get_text("\n", strip=True)

    linhas = limpar_linhas(texto)

    return "\n".join(linhas)


def extrair_doc_git(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()

    texto = soup.get_text("\n", strip=True)

    linhas = limpar_linhas(texto)

    inicio = 0

    for i, linha in enumerate(linhas):
        linha_lower = linha.lower()

        if "git clone" in linha_lower or "clone a repository" in linha_lower:
            inicio = i
            break

    fim = min(inicio + 120, len(linhas))
    trecho = linhas[inicio:fim]

    return "\n".join(trecho)


def extrair_doc_docker(html):
    texto = extrair_texto_generico(html)

    linhas = texto.splitlines()

    inicio = 0

    for i, linha in enumerate(linhas):
        if "docker" in linha.lower():
            inicio = i
            break

    fim = min(inicio + 120, len(linhas))

    return "\n".join(linhas[inicio:fim])


def extrair_doc_aws(html):
    texto = extrair_texto_generico(html)

    linhas = texto.splitlines()

    inicio = 0

    for i, linha in enumerate(linhas):
        if "amazon" in linha.lower() or "aws" in linha.lower():
            inicio = i
            break

    fim = min(inicio + 120, len(linhas))

    return "\n".join(linhas[inicio:fim])


def extrair_doc_kubernetes(html, assunto):
    texto = extrair_texto_generico(html)

    linhas = texto.splitlines()

    inicio = 0
    assunto_lower = assunto.lower()

    termos_busca = {
        "control-plane": ["control plane", "control-plane"],
        "kubectl": ["kubectl"],
        "pod": ["pod"],
        "deployment": ["deployment"],
        "service": ["service"],
        "namespace": ["namespace"],
        "configmap": ["configmap", "config map"],
        "secret": ["secret"],
        "ingress": ["ingress"],
        "node": ["node"],
    }

    termos = termos_busca.get(assunto_lower, [assunto_lower])

    for i, linha in enumerate(linhas):
        linha_lower = linha.lower()

        if any(termo in linha_lower for termo in termos):
            inicio = i
            break

    fim = min(inicio + 120, len(linhas))

    return "\n".join(linhas[inicio:fim])


def buscar_doc_online(comando):
    try:
        _, resto = comando.split(":", 1)
        tecnologia, assunto = resto.split("/", 1)

    except ValueError:
        return None, None, "Formato inválido. Use: webdoc:tecnologia/comando"

    tecnologia = tecnologia.lower().strip()
    assunto = assunto.lower().strip()

    headers = {"User-Agent": "DevOpsAssistant"}

    url = None

    if tecnologia == "git":
        url = f"https://git-scm.com/docs/git-{assunto}"

    elif tecnologia == "docker":
        aliases = {
            "run": "container/run",
            "build": "image/build",
            "pull": "image/pull",
            "push": "image/push",
            "exec": "container/exec",
            "ps": "container/ls",
            "logs": "container/logs",
            "images": "image/ls",
            "rm": "container/rm",
            "rmi": "image/rm",
            "start": "container/start",
            "stop": "container/stop",
            "restart": "container/restart",
            "inspect": "container/inspect",
        }

        caminho = aliases.get(assunto, assunto)

        url = f"https://docs.docker.com/reference/cli/docker/{caminho}/"

    elif tecnologia == "aws":
        aws_map = {
            "s3": "https://docs.aws.amazon.com/s3/",
            "ec2": "https://docs.aws.amazon.com/ec2/",
            "lambda": "https://docs.aws.amazon.com/lambda/",
            "iam": "https://docs.aws.amazon.com/iam/",
            "vpc": "https://docs.aws.amazon.com/vpc/",
            "ecs": "https://docs.aws.amazon.com/ecs/",
            "eks": "https://docs.aws.amazon.com/eks/",
            "rds": "https://docs.aws.amazon.com/rds/",
            "cloudwatch": "https://docs.aws.amazon.com/cloudwatch/",
            "cli": "https://docs.aws.amazon.com/cli/",
        }

        url = aws_map.get(assunto)

        if not url:
            return None, None, f"Serviço AWS não mapeado: {assunto}"

    elif tecnologia == "linux":
        try:
            resultado = subprocess.run(["man", assunto], capture_output=True, text=True)

            if resultado.returncode != 0:
                return None, None, f"Comando man não encontrado para: {assunto}"

            conteudo = resultado.stdout

            return f"man {assunto}", conteudo[:4000], None

        except Exception as erro:
            return None, None, f"Erro ao consultar man page: {erro}"

    elif tecnologia == "kubernetes":
        kubernetes_map = {
            "controlplane": "https://kubernetes.io/docs/concepts/architecture/#control-plane-component",
            "control-plane": "https://kubernetes.io/docs/concepts/architecture/#control-plane-component",
            "kubectl": "https://kubernetes.io/docs/reference/kubectl/",
            "pod": "https://kubernetes.io/docs/concepts/workloads/pods/",
            "deployment": "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/",
            "service": "https://kubernetes.io/docs/concepts/services-networking/service/",
            "namespace": "https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/",
            "configmap": "https://kubernetes.io/docs/concepts/configuration/configmap/",
            "secret": "https://kubernetes.io/docs/concepts/configuration/secret/",
            "ingress": "https://kubernetes.io/docs/concepts/services-networking/ingress/",
            "node": "https://kubernetes.io/docs/concepts/architecture/nodes/",
        }

        url = kubernetes_map.get(assunto)

        if not url:
            return None, None, f"Assunto Kubernetes não mapeado: {assunto}"

    else:
        return None, None, f"Tecnologia não suportada: {tecnologia}"

    try:
        resposta = requests.get(url, headers=headers, timeout=15)

        if resposta.status_code != 200:
            return None, None, f"Erro HTTP {resposta.status_code}"

        if tecnologia == "git":
            texto = extrair_doc_git(resposta.text)

        elif tecnologia == "docker":
            texto = extrair_doc_docker(resposta.text)

        elif tecnologia == "aws":
            texto = extrair_doc_aws(resposta.text)

        elif tecnologia == "kubernetes":
            texto = extrair_doc_kubernetes(resposta.text, assunto)

        else:
            texto = extrair_texto_generico(resposta.text)

        texto = remover_lixo_modelo(texto)

        if not texto:
            return None, None, "Não foi possível extrair texto da página."

        return url, texto[:7000], None

    except requests.RequestException as erro:
        return None, None, f"Erro de rede: {erro}"
