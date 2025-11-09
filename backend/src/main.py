import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager
from datetime import timedelta
from src.db import database 
from src.routers.documentos import documentos_router 

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.create_db_and_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    version='0.0.1',
    title='API-Gestión de documentos',
    description='Se crean y gestionan los documentos'
)

# Montar carpeta de archivos estáticos (por ejemplo PDFs)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/archivos", StaticFiles(directory=os.path.join(BASE_DIR, "archivos")), name="archivos")

app.add_middleware(
    SessionMiddleware,
    secret_key="clave_super_segura",
    max_age=int(timedelta(hours=1).total_seconds()),
    same_site="lax",
    https_only=False
)

app.include_router(documentos_router)
