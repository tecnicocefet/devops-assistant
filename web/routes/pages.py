from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from modules.code_analyzer.analyzer import analisar_texto_stream

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "pages/home.html",
        {"request": request}
    )


@router.get("/analyzer", response_class=HTMLResponse)
def analyzer_page(request: Request):
    return templates.TemplateResponse(
        "pages/analyzer.html",
        {"request": request}
    )


@router.get("/labs", response_class=HTMLResponse)
def labs_page(request: Request):
    return templates.TemplateResponse(
        "pages/labs.html",
        {"request": request}
    )


@router.get("/kb", response_class=HTMLResponse)
def kb_page(request: Request):
    return templates.TemplateResponse(
        "pages/kb.html",
        {"request": request}
    )


@router.post("/analyzer/run")
def run_analyzer(code: str = Form(...)):

    def gerar_resposta():
        stream = analisar_texto_stream(
            "deepseek-coder:6.7b",
            "snippet.sh",
            code
        )

        for chunk in stream:
            yield chunk

    return StreamingResponse(
        gerar_resposta(),
        media_type="text/plain; charset=utf-8"
    )