import json
import os
import re
import unicodedata
from datetime import datetime

BASE_DOCS_DIR = os.path.join("data", "docs")


def normalizar_slug(nome: str) -> str:
    nome = (nome or "").strip().lower()

    nome = unicodedata.normalize("NFKD", nome)
    nome = nome.encode("ascii", "ignore").decode("ascii")

    nome = nome.replace("/", "-")
    nome = nome.replace("_", "-")
    nome = re.sub(r"\s+", "-", nome)
    nome = re.sub(r"[^a-z0-9\-]", "", nome)
    nome = re.sub(r"-{2,}", "-", nome)
    nome = nome.strip("-")

    return nome


def normalizar_tecnologia(tecnologia: str) -> str:
    tecnologia = (tecnologia or "").strip().lower()

    tecnologia = unicodedata.normalize("NFKD", tecnologia)
    tecnologia = tecnologia.encode("ascii", "ignore").decode("ascii")

    tecnologia = tecnologia.replace("/", "-")
    tecnologia = tecnologia.replace("_", "-")
    tecnologia = re.sub(r"\s+", "-", tecnologia)
    tecnologia = re.sub(r"[^a-z0-9\-]", "", tecnologia)
    tecnologia = re.sub(r"-{2,}", "-", tecnologia)
    tecnologia = tecnologia.strip("-")

    return tecnologia


def obter_pasta_tecnologia(tecnologia: str) -> str:
    tecnologia_norm = normalizar_tecnologia(tecnologia)
    pasta = os.path.join(BASE_DOCS_DIR, tecnologia_norm)
    os.makedirs(pasta, exist_ok=True)
    return pasta


def obter_caminho_doc(tecnologia: str, comando: str) -> str:
    pasta = obter_pasta_tecnologia(tecnologia)
    slug = normalizar_slug(comando)
    return os.path.join(pasta, f"{slug}.md")


def obter_caminho_index(tecnologia: str) -> str:
    pasta = obter_pasta_tecnologia(tecnologia)
    return os.path.join(pasta, "_index.json")


def carregar_index(tecnologia: str) -> dict:
    caminho_index = obter_caminho_index(tecnologia)

    if not os.path.exists(caminho_index):
        return {
            "technology": normalizar_tecnologia(tecnologia),
            "items": [],
        }

    with open(caminho_index, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_index(tecnologia: str, index_data: dict) -> None:
    caminho_index = obter_caminho_index(tecnologia)

    with open(caminho_index, "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)


def atualizar_index(tecnologia: str, comando: str, source: str = "manual") -> None:
    index_data = carregar_index(tecnologia)
    slug = normalizar_slug(comando)
    agora = datetime.now().isoformat(timespec="seconds")

    items = index_data.get("items", [])
    existente = None

    for item in items:
        if item.get("slug") == slug:
            existente = item
            break

    if existente:
        existente["title"] = comando
        existente["source"] = source
        existente["updated_at"] = agora
    else:
        items.append(
            {
                "slug": slug,
                "title": comando,
                "source": source,
                "updated_at": agora,
            }
        )

    items.sort(key=lambda x: x.get("slug", ""))
    index_data["technology"] = normalizar_tecnologia(tecnologia)
    index_data["items"] = items

    salvar_index(tecnologia, index_data)


def salvar_doc(
    tecnologia: str, comando: str, conteudo: str, source: str = "manual"
) -> dict:
    caminho_doc = obter_caminho_doc(tecnologia, comando)

    with open(caminho_doc, "w", encoding="utf-8") as f:
        f.write((conteudo or "").strip() + "\n")

    atualizar_index(tecnologia, comando, source=source)

    return {
        "status": "saved",
        "technology": normalizar_tecnologia(tecnologia),
        "slug": normalizar_slug(comando),
        "path": caminho_doc,
    }


def ler_doc(tecnologia: str, comando: str) -> dict:
    caminho_doc = obter_caminho_doc(tecnologia, comando)

    if not os.path.exists(caminho_doc):
        return {
            "status": "not_found",
            "technology": normalizar_tecnologia(tecnologia),
            "slug": normalizar_slug(comando),
            "path": caminho_doc,
            "content": "",
        }

    with open(caminho_doc, "r", encoding="utf-8") as f:
        conteudo = f.read()

    return {
        "status": "ok",
        "technology": normalizar_tecnologia(tecnologia),
        "slug": normalizar_slug(comando),
        "path": caminho_doc,
        "content": conteudo,
    }


def listar_docs(tecnologia: str | None = None) -> list[dict]:
    docs = []

    if tecnologia:
        tecnologias = [normalizar_tecnologia(tecnologia)]
    else:
        if not os.path.exists(BASE_DOCS_DIR):
            return docs

        tecnologias = sorted(
            nome
            for nome in os.listdir(BASE_DOCS_DIR)
            if os.path.isdir(os.path.join(BASE_DOCS_DIR, nome))
        )

    for tech in tecnologias:
        index_data = carregar_index(tech)

        for item in index_data.get("items", []):
            slug = item.get("slug", "")
            docs.append(
                {
                    "technology": tech,
                    "slug": slug,
                    "title": item.get("title", slug),
                    "source": item.get("source", "manual"),
                    "updated_at": item.get("updated_at"),
                    "path": obter_caminho_doc(tech, slug),
                }
            )

    docs.sort(key=lambda x: (x["technology"], x["slug"]))
    return docs
