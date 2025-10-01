# api/database.py
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine

# 1. Definição do Modelo de Dados
class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    company: str
    location: str
    url: str

# 2. Configuração do Banco de Dados
DATABASE_URL = "sqlite:///jobs.db"
engine = create_engine(DATABASE_URL)