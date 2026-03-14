from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from modules.code_analyzer.analyzer import analisar_texto_stream, corrigir_texto_stream
from modules.lab_generator.generator import (
    gerar_lab_stream,
    salvar_lab_arquivo,
    listar_labs_salvos,
)

from modules.lab_generator.generator import (
    gerar_lab_stream,
    salvar_lab_arquivo,
    listar_labs_salvos,
    ler_lab_salvo,
)

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("pages/home.html", {"request": request})


@router.get("/analyzer", response_class=HTMLResponse)
def analyzer_page(request: Request):
    return templates.TemplateResponse("pages/analyzer.html", {"request": request})


@router.get("/labs", response_class=HTMLResponse)
def labs_page(request: Request):
    return templates.TemplateResponse("pages/labs.html", {"request": request})


@router.get("/kb", response_class=HTMLResponse)
def kb_page(request: Request):
    return templates.TemplateResponse("pages/kb.html", {"request": request})


@router.post("/analyzer/run")
def run_analyzer(code: str = Form(...)):

    def gerar_resposta():
        stream = analisar_texto_stream("deepseek-coder:6.7b", "snippet.txt", code)

        for chunk in stream:
            yield chunk

    return StreamingResponse(gerar_resposta(), media_type="text/plain; charset=utf-8")


@router.post("/analyzer/fix")
def fix_analyzer(code: str = Form(...)):

    def gerar_resposta():
        stream = corrigir_texto_stream("deepseek-coder:6.7b", "snippet.txt", code)

        for chunk in stream:
            yield chunk

    return StreamingResponse(gerar_resposta(), media_type="text/plain; charset=utf-8")


@router.post("/labs/run")
def run_lab(assunto: str = Form(...)):

    def gerar_resposta():
        stream = gerar_lab_stream(assunto, "deepseek-coder:6.7b")

        for chunk in stream:
            yield chunk

    return StreamingResponse(gerar_resposta(), media_type="text/plain; charset=utf-8")


@router.post("/labs/save")
async def save_lab(
    assunto: str = Form(...),
    conteudo: str = Form(...),
    modo: str = Form("fail"),
    novo_nome: str = Form(""),
):
    assunto = assunto.strip()

    if assunto.startswith("lab:"):
        assunto = assunto[len("lab:") :].strip()

    resultado = salvar_lab_arquivo(
        assunto=assunto,
        conteudo_lab=conteudo,
        modo=modo,
        novo_nome=novo_nome,
    )

    return resultado


@router.get("/labs/list")
def listar_labs():
    labs = listar_labs_salvos()
    return {"labs": labs}


@router.get("/labs/open")
def abrir_lab(tecnologia: str, nome: str):
    return ler_lab_salvo(tecnologia, nome)
