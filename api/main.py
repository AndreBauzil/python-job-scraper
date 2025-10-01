# api/main.py

from typing import List, Optional
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .database import Job, engine 
from . import analytics

from sqlmodel import Session, select

app = FastAPI(
    title="Job Scraper API",
    description="Uma API para enviar dados de vagas de emprego coletadas da web.",
    version="0.1.0",
)
origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Origens que podem fazer requisições
    allow_credentials=True,
    allow_methods=["*"], # Todos os métodos
    allow_headers=["*"], # Todos os cabeçalhos
)

app.include_router(analytics.router)

@app.get("/vagas", response_model=List[Job])
def get_vagas(
    title: Optional[str] = Query(None, description="Filtrar vagas por título que contenha o texto"),
    company: Optional[str] = Query(None, description="Filtrar vagas por empresa que contenha o texto")
):
    """
    Retorna uma lista de todas as vagas de emprego salvas no banco de dados.
    """
    with Session(engine) as session:
        statement = select(Job)

        if title:
            statement = statement.where(Job.title.contains(title))

        if company:
            statement = statement.where(Job.company.contains(company))

        results = session.exec(statement)
        jobs = results.all()
        return jobs
