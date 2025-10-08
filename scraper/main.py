# scraper/main.py

import time
from typing import Optional
import httpx
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    company: str
    location: str
    url: str = Field(unique=True)

DATABASE_URL = "sqlite:///jobs.db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def run_linkedin_scraper():
    """
    Coleta vagas de emprego do LinkedIn usando Playwright para lidar com conteúdo dinâmico
    e salva no banco de dados.
    """
    url = "https://br.linkedin.com/jobs/search?keywords=&geoId=102556749&f_E=2&f_TPR=r86400&sortBy=R"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()

        print(f"Acessando a página: {url}")
        page.goto(url, timeout=90000)

        print("Página acessada. Tentando fechar modais e rolar a página...")

        try:
            modal_close_button_selector = "button.modal__dismiss"
            page.wait_for_selector(modal_close_button_selector, timeout=5000)
            page.click(modal_close_button_selector)
            print("Modal de login fechado.")
        except TimeoutError:
            print("Nenhum modal de login encontrado, continuando...")

        for _ in range(5): # Rola 5x
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)

        list_selector = "ul.jobs-search__results-list"
        page.wait_for_selector(list_selector)

        print("Coletando o HTML final da página...")
        page_content = page.content()

        soup = BeautifulSoup(page_content, "lxml")

        job_cards = soup.select('div.base-search-card')

        print(f"Encontradas {len(job_cards)} vagas na página. Salvando no banco de dados...")

        new_jobs_found = 0
        with Session(engine) as session:
            for card in job_cards:
                title_element = card.select_one("h3.base-search-card__title")
                company_element = card.select_one("h4.base-search-card__subtitle a")
                location_element = card.select_one("span.job-search-card__location")
                url_element = card.select_one("a.base-card__full-link")

                title = title_element.text.strip() if title_element else "N/A"
                company = company_element.text.strip() if company_element else "N/A"
                location = location_element.text.strip() if location_element else "N/A"
                url = url_element['href'] if url_element else "N/A"

                if title != "N/A" and url != "N/A":
                    # Vaga já existe?
                    statement = select(Job).where(Job.url == url)
                    existing_job = session.exec(statement).first()

                    if not existing_job:
                        job = Job(title=title, company=company, location=location, url=url)
                        session.add(job)
                        new_jobs_found += 1

            session.commit()

        print(f"Coleta finalizada. {new_jobs_found} novas vagas foram adicionadas ao banco de dados.")
        browser.close()


if __name__ == "__main__":
    print("Preparando o banco de dados...")
    create_db_and_tables()
    run_linkedin_scraper()
