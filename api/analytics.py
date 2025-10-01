# api/analytics.py

from fastapi import APIRouter
from sqlmodel import Session, select
from sqlalchemy.sql import func
from sqlalchemy import desc

from .database import engine, Job

# "Roteador" para organizar endpoints de analytics
router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)

@router.get("/top-cities")
def get_top_cities():
    """
    Retorna as 5 cidades com o maior número de vagas,
    agrupadas e contadas.
    """
    with Session(engine) as session:
        statement = (
            select(Job.location, func.count(Job.id).label("job_count"))
            .group_by(Job.location)
            .order_by(desc("job_count"))
            .limit(5)
        )
        results = session.exec(statement).all()
        formatted_results = [
            {"city": location, "jobs": job_count}
            for location, job_count in results
        ]
        return formatted_results
