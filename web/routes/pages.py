from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from modules.code_analyzer.analyzer import analisar_texto_stream, corrigir_texto_stream
from modules.lab_generator.generator import (
    gerar_lab_stream,
    salvar_lab_arquivo,
    listar_labs_salvos,
    ler_lab_salvo,
)
from modules.doc_reader.reader import (
    buscar_doc_em_data,
    melhorar_doc_em_data,
    melhorar_doc_em_data_stream,
    salvar_doc_em_data,
)
from modules.man_reader.reader import (
    ler_man_page,
    explicar_man_page,
    salvar_man_como_doc,
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


@router.get("/reader", response_class=HTMLResponse)
def reader_page(request: Request):
    return templates.TemplateResponse("pages/reader.html", {"request": request})


@router.post("/analyzer/run")
def run_analyzer(code: str = Form(...)):
    def gerar_resposta():
        for chunk in analisar_texto_stream(
            "deepseek-coder:6.7b",
            "snippet.txt",
            code,
        ):
            if chunk:
                yield chunk

    return StreamingResponse(
        gerar_resposta(),
        media_type="text/plain; charset=utf-8",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@router.post("/analyzer/fix")
def fix_analyzer(code: str = Form(...)):
    def gerar_resposta():
        for chunk in corrigir_texto_stream(
            "deepseek-coder:6.7b",
            "snippet.txt",
            code,
        ):
            if chunk:
                yield chunk

    return StreamingResponse(
        gerar_resposta(),
        media_type="text/plain; charset=utf-8",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@router.post("/labs/run")
def run_lab(assunto: str = Form(...)):
    def gerar_resposta():
        for chunk in gerar_lab_stream(assunto, "deepseek-coder:6.7b"):
            if chunk:
                yield chunk

    return StreamingResponse(
        gerar_resposta(),
        media_type="text/plain; charset=utf-8",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


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


@router.post("/reader/doc")
def reader_doc(assunto: str = Form(...)):
    def gerar_resposta():
        try:
            caminho, conteudo = buscar_doc_em_data(assunto)

            if conteudo:
                yield conteudo
            else:
                yield f"Documentação não encontrada para: {assunto}"

        except Exception as erro:
            yield f"Erro ao ler documentação: {erro}"

    return StreamingResponse(
        gerar_resposta(),
        media_type="text/plain; charset=utf-8",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@router.post("/reader/doc/improve")
def reader_doc_improve(assunto: str = Form(...)):
    def gerar_resposta():
        try:
            for chunk in melhorar_doc_em_data_stream(
                assunto,
                modelo="deepseek-coder:6.7b",
            ):
                yield chunk
        except Exception as erro:
            yield f"Erro ao melhorar documentação: {erro}"

    return StreamingResponse(
        gerar_resposta(),
        media_type="text/plain; charset=utf-8",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )

@router.post("/reader/doc/save")
async def reader_doc_save(
    assunto: str = Form(...),
    conteudo: str = Form(...),
):
    return salvar_doc_em_data(assunto, conteudo)


@router.post("/reader/man")
def reader_man(comando: str = Form(...)):
    def gerar_resposta():
        try:
            conteudo, erro = ler_man_page(comando)

            if erro:
                yield erro
            else:
                yield conteudo

        except Exception as erro:
            yield f"Erro ao consultar man page: {erro}"

    return StreamingResponse(
        gerar_resposta(),
        media_type="text/plain; charset=utf-8",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@router.post("/reader/man/explain")
def reader_man_explain(comando: str = Form(...)):
    def gerar_resposta():
        try:
            conteudo, erro = explicar_man_page(
                comando,
                modelo="deepseek-coder:6.7b",
            )

            if erro:
                yield erro
            else:
                yield conteudo

        except Exception as erro:
            yield f"Erro ao explicar man page: {erro}"

    return StreamingResponse(
        gerar_resposta(),
        media_type="text/plain; charset=utf-8",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@router.post("/reader/man/save")
async def reader_man_save(
    comando: str = Form(...),
    conteudo: str = Form(...),
):
    return salvar_man_como_doc(comando, conteudo)
