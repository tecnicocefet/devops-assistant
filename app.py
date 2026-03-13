from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from web.routes.pages import router as pages_router

app = FastAPI(title="DevOps Assistant Web")

app.mount("/static", StaticFiles(directory="web/static"), name="static")

app.include_router(pages_router)