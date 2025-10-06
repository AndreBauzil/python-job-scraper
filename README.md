# Job Scraper & Analytics Dashboard

**Status do Projeto: Concluído (Versão 1.0)**

Este projeto é um sistema full-stack de automação e análise de dados. Ele consiste em um web scraper desenvolvido em Python que coleta vagas de emprego de sites públicos, uma API RESTful (também em Python) para servir esses dados, e um dashboard interativo em React para visualização e filtragem.

### Screenshots

| Dashboard de Análise | Documentação da API (Automática) |
| :---: | :---: |
| ![Dashboard de Análise](./assets/) | ![Documentação da API](./assets/) |

*(Instrução: Adicione os prints na raiz do projeto ou em uma pasta `assets` e atualize os caminhos. Recomendo tirar um print do dashboard e outro da página `http://localhost:8000/docs` para mostrar a documentação automática do FastAPI).*

---

### Destaques para Recrutadores

Este projeto foi desenvolvido para demonstrar um conjunto de habilidades que vão além de um simples CRUD, focando em arquitetura de sistemas, engenharia de dados e visualização.

* **Arquitetura Full-Stack Poliglota:** Demonstra a capacidade de integrar um backend em **Python (FastAPI)** com um frontend em **JavaScript/TypeScript (React)**, uma arquitetura comum em microserviços.
* **Engenharia de Dados (Ponta a Ponta):** Cobre o ciclo de vida completo de um projeto de dados:
    * **Coleta:** Web scraping com `BeautifulSoup` e `HTTPX`.
    * **Armazenamento:** Persistência de dados em um banco de dados relacional (SQLite/PostgreSQL) gerenciado via ORM com **SQLModel**.
    * **Processamento:** Lógica de agregação no backend para gerar analytics (ex: contagem de vagas por cidade).
    * **Visualização:** Apresentação dos dados brutos e agregados em um dashboard com tabelas, filtros e gráficos (`Recharts`).
* **API RESTful Moderna:** A API desenvolvida com **FastAPI** inclui documentação interativa automática (Swagger UI), validação de dados com Pydantic e boas práticas de design de API.
* **Boas Práticas de Desenvolvimento Python:** Uso de ambientes virtuais (`venv`), modularização do código (roteadores, serviços) e ORM para interação segura com o banco de dados.
* **Frontend Reativo e Profissional:** Utilização da mesma stack moderna do projeto anterior (**Vite, React, TypeScript, Tailwind CSS, Shadcn/ui**), demonstrando consistência e domínio das ferramentas.

---

### Tecnologias Utilizadas

#### **Backend**
* **Python 3.11+**
* **FastAPI** (Framework da API)
* **Uvicorn** (Servidor ASGI)
* **SQLModel** (ORM) & **SQLAlchemy**
* **HTTPX** (Cliente HTTP)
* **BeautifulSoup4** (HTML Parsing)
* **SQLite** (Banco de Dados)

#### **Frontend**
* **React**
* **Vite**
* **TypeScript**
* **Tailwind CSS**
* **Shadcn/ui** (Biblioteca de Componentes)
* **Recharts** (Gráficos)
* **Axios** (Cliente HTTP)

---

### Funcionalidades Implementadas

* **Web Scraper:** Script automatizado que coleta vagas de emprego do site `python.org/jobs`.
* **API RESTful:**
    * Endpoint `GET /vagas` com filtros dinâmicos por título e empresa.
    * Endpoint de analytics `GET /analytics/top-cities` para dados do gráfico.
    * Documentação interativa automática em `/docs`.
* **Dashboard Interativo:**
    * Tabela com todas as vagas coletadas.
    * Filtros em tempo real.
    * Cards com métricas (Total de vagas, empresas únicas).
    * Gráfico de barras com o "Top 5 Cidades com Mais Vagas".

---

### Como Executar o Projeto Localmente

*(As instruções de setup continuam as mesmas)*