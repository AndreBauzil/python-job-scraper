# scraper/main.py

from typing import Optional
import httpx
from bs4 import BeautifulSoup
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    company: str
    location: str
    url: str

DATABASE_URL = "sqlite:///jobs.db"
engine = create_engine(DATABASE_URL)

def clean_location_string(location: str) -> str:
    """Remove duplicatas de uma string de localização separada por vírgulas."""
    if not location:
        return "N/A"
    # Converte p/ minúsculas, divide por vírgula, remove espaços, remove duplicatas e junta
    parts = [part.strip() for part in location.lower().split(',')]
    unique_parts = sorted(list(set(parts)), key=parts.index)

    return ', '.join(part.capitalize() for part in unique_parts)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def run_scraper():
    """
    Coleta as vagas de emprego do site Python.org e as salva no banco de dados.
    """
    URL_TARGET = "https://www.python.org/jobs/"

    print("Iniciando a coleta de vagas...")

    response = httpx.get(URL_TARGET)

    if response.status_code != 200:
        print(f"Erro ao acessar a página. Status: {response.status_code}")
        return

    print("Página acessada com sucesso. Analisando o HTML...")

    soup = BeautifulSoup(response.content, "lxml")

    job_list = soup.select(".list-recent-jobs > li")

    new_jobs_found = 0

    with Session(engine) as session:
        for job_item in job_list:
            title_element = job_item.select_one("span.listing-company-name > a")

            if "New " in title_element.text:
                title = title_element.text.replace("New ", "").strip()
            else:
                title = title_element.text

            br_tag = job_item.find("br")
            company_text = br_tag.next_sibling.strip() if br_tag and br_tag.next_sibling else ""

            location_element = job_item.select_one("span.listing-location")
            location = location_element.text.strip() if location_element else "N/A"

            location = clean_location_string(location)

            company = company_text if company_text else "N/A"
            title = title_element.text.strip() if title_element else "N/A"
            url = f"https://www.python.org{title_element['href']}" if title_element else "N/A"

            statement = select(Job).where(Job.url == url)
            existing_job = session.exec(statement).first()

            if existing_job:
                continue

            job = Job(title=title, company=company, location=location, url=url)
            session.add(job)
            new_jobs_found += 1

        session.commit()

    print(f"Coleta Finalizada. {new_jobs_found} novas vagas formas salvas no banco de dados.")

if __name__ == "__main__":
    print("Preparando o banco de dados...")
    create_db_and_tables()
    run_scraper()
