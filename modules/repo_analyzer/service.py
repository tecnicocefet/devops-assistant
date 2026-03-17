import os
from pathlib import Path
import time
import tempfile
import shutil
import subprocess


PASTAS_IGNORADAS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".terraform",
    ".vagrant",
    "dist",
    "build",
}

ARQUIVOS_PRIORITARIOS = {
    "dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "makefile",
    ".env.example",
    "readme.md",
    "vagrantfile",
}

PALAVRAS_PRIORITARIAS = {
    "zabbix",
    "grafana",
    "prometheus",
    "ansible",
    "terraform",
    "docker",
    "kubernetes",
    "nginx",
    "mysql",
    "postgres",
    "vagrant",
    "aws",
}

EXTENSOES_PRIORITARIAS = {
    ".tf",
    ".sh",
    ".yml",
    ".yaml",
    ".j2",
}

MAX_ARQUIVOS_LIDOS = 12
MAX_ITENS_POR_SECAO = 8


def caminho_repo_valido(caminho: str):
    if not caminho or not caminho.strip():
        return False, "Caminho do repositório não informado."

    repo_path = Path(caminho).expanduser().resolve()

    if not repo_path.exists():
        return False, f"Caminho não encontrado: {repo_path}"

    if not repo_path.is_dir():
        return False, f"O caminho informado não é uma pasta: {repo_path}"

    return True, str(repo_path)


def eh_url_github(origem: str):
    if not origem:
        return False

    origem = origem.strip().lower()

    return origem.startswith("https://github.com/") or origem.startswith(
        "http://github.com/"
    )


def extrair_nome_repo_da_url(url_repo: str):
    nome = url_repo.rstrip("/").split("/")[-1]

    if nome.endswith(".git"):
        nome = nome[:-4]

    return nome or "repo"


def clonar_repo_temporario(url_repo: str):
    pasta_base = tempfile.mkdtemp(prefix="repo_analyzer_")
    nome_pasta = extrair_nome_repo_da_url(url_repo)
    destino = os.path.join(pasta_base, nome_pasta)

    try:
        resultado = subprocess.run(
            ["git", "clone", "--depth", "1", url_repo, destino],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if resultado.returncode != 0:
            shutil.rmtree(pasta_base, ignore_errors=True)
            erro = resultado.stderr.strip() or "Falha ao clonar repositório remoto."
            return {
                "ok": False,
                "erro": erro,
                "repo_path": None,
                "temp_dir": None,
            }

        return {
            "ok": True,
            "erro": None,
            "repo_path": destino,
            "temp_dir": pasta_base,
        }

    except Exception as e:
        shutil.rmtree(pasta_base, ignore_errors=True)
        return {
            "ok": False,
            "erro": f"Erro ao clonar repositório remoto: {e}",
            "repo_path": None,
            "temp_dir": None,
        }


def deve_ignorar_pasta(nome_pasta: str):
    return nome_pasta.lower() in PASTAS_IGNORADAS


def eh_arquivo_relevante(nome_arquivo: str):
    nome_lower = nome_arquivo.lower()

    if nome_lower in ARQUIVOS_PRIORITARIOS:
        return True

    sufixo = Path(nome_lower).suffix
    if sufixo in EXTENSOES_PRIORITARIAS:
        return True

    return False


def calcular_score_arquivo(caminho_arquivo: str, repo_path: str):
    relativo = os.path.relpath(caminho_arquivo, repo_path).lower()
    nome = os.path.basename(caminho_arquivo).lower()

    score = 0

    if nome in ARQUIVOS_PRIORITARIOS:
        score += 50

    if Path(nome).suffix in EXTENSOES_PRIORITARIAS:
        score += 20

    for palavra in PALAVRAS_PRIORITARIAS:
        if palavra in relativo:
            score += 30

    if "roles" in relativo:
        score += 15

    if "templates" in relativo:
        score += 10

    if "playbook" in relativo:
        score += 15

    return score


def listar_arquivos_relevantes(repo_path: str):
    arquivos_encontrados = []

    for raiz, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if not deve_ignorar_pasta(d)]

        for nome_arquivo in files:
            caminho_completo = os.path.join(raiz, nome_arquivo)

            if eh_arquivo_relevante(nome_arquivo):
                arquivos_encontrados.append(caminho_completo)
                continue

            relativo = os.path.relpath(caminho_completo, repo_path).lower()
            if any(palavra in relativo for palavra in PALAVRAS_PRIORITARIAS):
                arquivos_encontrados.append(caminho_completo)

    arquivos_encontrados = sorted(
        arquivos_encontrados,
        key=lambda caminho: calcular_score_arquivo(caminho, repo_path),
        reverse=True,
    )

    return arquivos_encontrados[:MAX_ARQUIVOS_LIDOS]


def detectar_evidencias_repo(repo_path: str, arquivos: list[str]):
    nome_repo = Path(repo_path).name.lower()
    caminhos_relativos = [
        os.path.relpath(caminho, repo_path).lower() for caminho in arquivos
    ]

    evidencias = {
        "terraform": False,
        "ansible": False,
        "zabbix": False,
        "grafana": False,
        "prometheus": False,
        "docker": False,
        "kubernetes": False,
        "nginx": False,
        "mysql": False,
        "postgres": False,
        "vagrant": False,
        "aws": False,
    }

    for tecnologia in evidencias.keys():
        if tecnologia in nome_repo:
            evidencias[tecnologia] = True
            continue

        for relativo in caminhos_relativos:
            if tecnologia in relativo:
                evidencias[tecnologia] = True
                break

    return evidencias


def agrupar_arquivos_por_area(arquivos_relativos: list[str]):
    grupos = {
        "infra": [],
        "provisionamento": [],
        "monitoramento": [],
        "banco_de_dados": [],
        "templates": [],
        "configs": [],
        "outros": [],
    }

    for arquivo in arquivos_relativos:
        caminho = arquivo.lower()

        if "vagrant" in caminho or caminho.endswith("vagrantfile") or ".tf" in caminho:
            grupos["infra"].append(arquivo)
        elif "ansible" in caminho or "playbook" in caminho or "roles/" in caminho:
            grupos["provisionamento"].append(arquivo)
        elif (
            "zabbix" in caminho
            or "grafana" in caminho
            or "prometheus" in caminho
            or "nginx" in caminho
        ):
            grupos["monitoramento"].append(arquivo)
        elif "mysql" in caminho or "postgres" in caminho:
            grupos["banco_de_dados"].append(arquivo)
        elif "templates/" in caminho or caminho.endswith(".j2"):
            grupos["templates"].append(arquivo)
        elif caminho.endswith((".yml", ".yaml", ".conf", ".ini")):
            grupos["configs"].append(arquivo)
        else:
            grupos["outros"].append(arquivo)

    return {k: v for k, v in grupos.items() if v}


def gerar_resumo_repo(repo_path: str, arquivos: list[str], evidencias: dict):
    nome_repo = Path(repo_path).name
    tecnologias = [nome for nome, presente in evidencias.items() if presente]
    arquivos_relativos = [os.path.relpath(a, repo_path) for a in arquivos]
    grupos = agrupar_arquivos_por_area(arquivos_relativos)

    resumo = {
        "nome_repositorio": nome_repo,
        "tecnologias_detectadas": tecnologias,
        "arquivos_relevantes": arquivos_relativos[:MAX_ARQUIVOS_LIDOS],
        "grupos": grupos,
    }

    return resumo


def gerar_badges_tecnologias(tecnologias: list[str]):
    badges = {
        "terraform": "![Terraform](https://img.shields.io/badge/Terraform-623CE4?logo=terraform&logoColor=white)",
        "aws": "![AWS](https://img.shields.io/badge/AWS-232F3E?logo=amazonaws&logoColor=white)",
        "docker": "![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)",
        "ansible": "![Ansible](https://img.shields.io/badge/Ansible-EE0000?logo=ansible&logoColor=white)",
        "kubernetes": "![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)",
        "grafana": "![Grafana](https://img.shields.io/badge/Grafana-F46800?logo=grafana&logoColor=white)",
        "prometheus": "![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white)",
        "nginx": "![Nginx](https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white)",
        "mysql": "![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white)",
        "postgres": "![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)",
        "zabbix": "![Zabbix](https://img.shields.io/badge/Zabbix-CC0000?logo=zabbix&logoColor=white)",
        "vagrant": "![Vagrant](https://img.shields.io/badge/Vagrant-1563FF?logo=vagrant&logoColor=white)",
    }

    badges_gerados = []

    for tech in tecnologias:
        if tech in badges:
            badges_gerados.append(badges[tech])

    return "\n".join(badges_gerados)


def montar_contexto_repo(repo_path: str):
    arquivos = listar_arquivos_relevantes(repo_path)

    if not arquivos:
        return {
            "ok": False,
            "erro": "Nenhum arquivo relevante encontrado no repositório.",
            "repo_path": repo_path,
            "arquivos": [],
            "contexto": "",
            "resumo": None,
        }

    nome_repo = Path(repo_path).name
    evidencias = detectar_evidencias_repo(repo_path, arquivos)
    resumo = gerar_resumo_repo(repo_path, arquivos, evidencias)

    blocos = []
    blocos.append(f"REPOSITORIO: {nome_repo}")
    blocos.append("")

    blocos.append("RESUMO ESTRUTURAL:")
    blocos.append(f"- Nome do repositório: {resumo['nome_repositorio']}")

    if resumo["tecnologias_detectadas"]:
        blocos.append(
            "- Tecnologias detectadas: " + ", ".join(resumo["tecnologias_detectadas"])
        )
    else:
        blocos.append("- Tecnologias detectadas: nenhuma")

    blocos.append("")

    blocos.append("ARQUIVOS RELEVANTES:")
    for arq in resumo["arquivos_relevantes"]:
        blocos.append(f"- {arq}")

    blocos.append("")

    blocos.append("AGRUPAMENTO FUNCIONAL:")
    for grupo, itens in resumo["grupos"].items():
        blocos.append(f"- {grupo}:")
        for item in itens[:MAX_ITENS_POR_SECAO]:
            blocos.append(f"  - {item}")

    blocos.append("")
    blocos.append("EVIDENCIAS CONFIRMADAS:")
    blocos.append(f"- Nome do repositório: {nome_repo}")

    tecnologias_detectadas = [nome for nome, presente in evidencias.items() if presente]
    if tecnologias_detectadas:
        blocos.append(
            "- Tecnologias com evidência no nome do repositório ou nos caminhos: "
            + ", ".join(tecnologias_detectadas)
        )
    else:
        blocos.append(
            "- Nenhuma tecnologia prioritária detectada no nome do repositório ou nos caminhos."
        )

    blocos.append("")
    blocos.append("REGRAS DE INTERPRETACAO:")
    blocos.append("- Use apenas informações com evidência explícita neste contexto.")
    blocos.append("- Não invente comandos.")
    blocos.append("- Não invente pré-requisitos.")
    blocos.append("- Não invente instalação.")
    blocos.append("- Não invente contribuição.")
    blocos.append("- Não invente licença.")
    blocos.append("- Não cite tecnologias sem evidência explícita.")
    blocos.append(
        "- Não descreva arquivos ocultos de cache ou diretórios internos do Vagrant."
    )
    blocos.append("- Seja direto e técnico.")
    blocos.append("")

    return {
        "ok": True,
        "erro": None,
        "repo_path": repo_path,
        "arquivos": arquivos,
        "contexto": "\n".join(blocos).strip(),
        "resumo": resumo,
    }


def gerar_prompt_readme_repo(repo_path: str):
    inicio_total = time.time()

    inicio_contexto = time.time()
    resultado = montar_contexto_repo(repo_path)
    fim_contexto = time.time()

    print(f"DEBUG tempo montar_contexto_repo: {fim_contexto - inicio_contexto:.2f}s")

    if not resultado["ok"]:
        return resultado

    contexto = resultado["contexto"]

    prompt = f"""
Você vai gerar apenas o CONTEÚDO de um README.md em markdown.

Escreva em português do Brasil.

IMPORTANTE:
- NÃO escreva o título do projeto.
- NÃO escreva badges.
- NÃO crie seção de tecnologias identificadas.
- NÃO repita lista de tecnologias detectadas.
- NÃO invente comandos.
- NÃO invente dependências.
- NÃO invente instalação.
- NÃO invente contribuição.
- NÃO invente licença.
- NÃO invente arquivos.
- Use somente informações com evidência explícita no contexto.
- Seja direto, técnico e específico.
- Se a evidência for fraca, use linguagem neutra.
- Não mencione diretórios internos como .vagrant, .git, cache, build ou artefatos temporários.

ESTRUTURA EXATA DA RESPOSTA:
## Visão geral
## Estrutura do projeto
## Observações

REGRAS POR SEÇÃO:

## Visão geral
- Explique em 2 a 4 linhas o objetivo provável do repositório.
- Cite apenas o que estiver claramente indicado pelo nome do repositório e pelos caminhos dos arquivos.

## Estrutura do projeto
- Liste os diretórios e arquivos mais relevantes.
- Explique o papel deles de forma curta.
- Ignore arquivos internos de ferramenta e arquivos irrelevantes.

## Observações
- Traga no máximo 3 observações curtas.
- Só mencione limitações ou contexto inferível pelas evidências.
- Não invente execução se não houver comando explícito.

Contexto:
{contexto}
""".strip()

    fim_total = time.time()
    print(f"DEBUG tempo gerar_prompt_readme_repo: {fim_total - inicio_total:.2f}s")
    print(f"DEBUG prompt size: {len(prompt)} chars")

    evidencias = detectar_evidencias_repo(repo_path, resultado["arquivos"])
    tecnologias_detectadas = [nome for nome, presente in evidencias.items() if presente]
    badges = gerar_badges_tecnologias(tecnologias_detectadas)

    return {
        "ok": True,
        "erro": None,
        "repo_path": repo_path,
        "arquivos": resultado["arquivos"],
        "contexto": contexto,
        "prompt": prompt,
        "badges": badges,
    }


def limpar_saida_readme(llm_output: str):
    if not llm_output:
        return ""

    linhas = llm_output.strip().splitlines()
    linhas_filtradas = []

    for linha in linhas:
        linha_strip = linha.strip()
        linha_lower = linha_strip.lower()

        if linha_lower.startswith("# "):
            continue

        if linha_lower.startswith("## tecnologias identificadas"):
            continue

        if linha_strip.startswith("!["):
            continue

        linhas_filtradas.append(linha)

    texto = "\n".join(linhas_filtradas).strip()

    while "\n\n\n" in texto:
        texto = texto.replace("\n\n\n", "\n\n")

    return texto.strip()


def montar_readme_final(repo_path: str, conteudo_llm: str, badges: str):
    nome_repo = Path(repo_path).name
    conteudo_limpo = limpar_saida_readme(conteudo_llm)

    partes = [f"# {nome_repo}"]

    if badges:
        partes.append(badges)

    if conteudo_limpo:
        partes.append(conteudo_limpo)

    return "\n\n".join(partes).strip() + "\n"


def preparar_readme_repo(origem: str):
    temp_dir = None

    if eh_url_github(origem):
        clone = clonar_repo_temporario(origem)

        if not clone["ok"]:
            return {
                "ok": False,
                "erro": clone["erro"],
                "prompt": None,
                "repo_path": None,
                "temp_dir": None,
                "badges": "",
            }

        repo_path = clone["repo_path"]
        temp_dir = clone["temp_dir"]
    else:
        valido, resultado = caminho_repo_valido(origem)

        if not valido:
            return {
                "ok": False,
                "erro": resultado,
                "prompt": None,
                "repo_path": None,
                "temp_dir": None,
                "badges": "",
            }

        repo_path = resultado

    resultado_prompt = gerar_prompt_readme_repo(repo_path)

    if temp_dir:
        resultado_prompt["temp_dir"] = temp_dir

    return resultado_prompt
