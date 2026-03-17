from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("pages/home.html", {"request": request})


@router.get("/analyzer", response_class=HTMLResponse)
def analyzer_page(request: Request):
    return templates.TemplateResponse("pages/analyzer.html", {"request": request})


@router.get("/reader", response_class=HTMLResponse)
def reader_page(request: Request):
    return templates.TemplateResponse("pages/reader.html", {"request": request})


@router.get("/labs", response_class=HTMLResponse)
def labs_page(request: Request):
    return templates.TemplateResponse("pages/labs.html", {"request": request})


@router.get("/kb", response_class=HTMLResponse)
def kb_page(request: Request):
    return templates.TemplateResponse("pages/kb.html", {"request": request})


@router.get("/docs", response_class=HTMLResponse)
def docs_page(request: Request):
    return templates.TemplateResponse("pages/docs.html", {"request": request})
