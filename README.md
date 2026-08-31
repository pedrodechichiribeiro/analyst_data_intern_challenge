# AI-Powered Data Analysis Dashboard

**English** · [Português](#português)

---

## English

Hi, I'm **Pedro Dechichi Ribeiro**.

This project started as my solution to a technical challenge in an internship selection process. I didn't get the position, but what I had built had enough substance to become a real portfolio project, so I kept developing it.

The result is a desktop dashboard for technical support ticket analysis that combines SQL, data visualization, and a cloud AI agent to generate executive reports automatically.

---

### What the project does

The application loads two JSON datasets containing anonymized support ticket data, processes everything through an in-memory SQLite database, displays 9 interactive visualizations and, at the click of a button, sends the context of the active chart to Google Gemini, which returns an analysis covering risks, trends, and operational recommendations.

The full pipeline is: raw data → SQL → chart → AI → insight.

---

### Available visualizations

Accessible from the top navigation bar:

1. **Top Products** — products with the highest ticket volume
2. **Severity Stack** — severity distribution per product
3. **Case Types** — ticket categories (bug, question, training...)
4. **Global Hotspots** — countries with the heaviest support load
5. **Ticket Density** — average tickets per account by region
6. **Industry Struggles** — support volume by market sector
7. **Volume Trend** — weekly trend of new tickets, plus a forward projection
8. **Resolution Time** — histogram of days until the ticket is closed
9. **Backlog Growth** — cumulative opened vs. closed tickets over time

---

### AI agent

Each visualization carries its own `system_prompt` and `data_context`. Clicking **"Generate Deep Analysis"** sends that data to an [Agno](https://github.com/agno-agi/agno) agent configured with the **Gemini 2.5 Flash** model, which acts as a senior support operations analyst.

The analysis runs on a separate thread so the interface never freezes.

---

### Project structure

```
├── data/
│   ├── accounts_anonymized.json
│   └── support_cases_anonymized.json
├── src/
│   ├── main.py           # Interface and layout (CustomTkinter)
│   ├── data_manager.py   # JSON loading and in-memory SQLite database
│   ├── graphs.py         # SQL queries + plotting logic (Matplotlib)
│   └── ai_analyst.py     # Agno agent + Gemini configuration
├── .env                  # API key (not versioned)
├── requirements.txt
└── README.md
```

---

### How to run

**Prerequisites:** Python 3.10+ and a [Google AI Studio API key](https://aistudio.google.com/) (a free tier is available).

```bash
# 1. Clone the repository
git clone https://github.com/pedrodechichiribeiro/analyst_data_intern_challenge
cd analyst_data_intern_challenge

# 2. Create and activate the virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 3. Install the dependencies
pip install -r requirements.txt

# 4. Set up the API key
# Create a .env file in the root directory containing:
GOOGLE_API_KEY=your_key_here_AIza...

# 5. Run it
python src/main.py
```

**With Docker:** see `README_DOCKER.md` for instructions on running the GUI through X11 forwarding.

---

### Stack

Python · CustomTkinter · Matplotlib · Pandas · SQLite · Agno · Google Gemini 2.5 Flash · python-dotenv

---

— Pedro

<br>

---

## Português

Olá, sou **Pedro Dechichi Ribeiro**.

Esse projeto nasceu como solução para um desafio técnico de processo seletivo de estágio. Não passei, mas o que construí tinha substância suficiente para virar um projeto de portfólio real — então continuei desenvolvendo.

O resultado é um dashboard desktop de análise de tickets de suporte técnico, que combina SQL, visualização de dados e um agente de IA em nuvem para gerar relatórios executivos automaticamente.

---

### O que o projeto faz

A aplicação carrega dois datasets JSON com dados anonimizados de chamados de suporte, processa tudo via SQLite em memória, exibe 9 visualizações interativas e, ao clicar num botão, envia o contexto do gráfico ativo para o Google Gemini — que retorna uma análise com riscos, tendências e recomendações operacionais.

O fluxo completo é: dados brutos → SQL → gráfico → IA → insight.

---

### Visualizações disponíveis

Acessíveis pela barra de navegação superior:

1. **Top Products** — produtos com maior volume de chamados
2. **Severity Stack** — distribuição de severidade por produto
3. **Case Types** — categorias de chamado (bug, dúvida, treinamento...)
4. **Global Hotspots** — países com maior carga de suporte
5. **Ticket Density** — média de tickets por conta por região
6. **Industry Struggles** — volume de suporte por setor de mercado
7. **Volume Trend** — tendência semanal de novos chamados + projeção futura
8. **Resolution Time** — histograma de dias até o fechamento do ticket
9. **Backlog Growth** — acumulado de abertos vs. fechados ao longo do tempo

---

### Agente de IA

Cada visualização carrega um `system_prompt` e um `data_context` específicos. Ao clicar em **"Generate Deep Analysis"**, esses dados são enviados para um agente [Agno](https://github.com/agno-agi/agno) configurado com o modelo **Gemini 2.5 Flash**, que atua como analista sênior de operações de suporte.

A análise roda em thread separada para não travar a interface.

---

### Estrutura do projeto

```
├── data/
│   ├── accounts_anonymized.json
│   └── support_cases_anonymized.json
├── src/
│   ├── main.py                    # Interface e layout (CustomTkinter)
│   ├── data_manager.py            # Carga dos JSONs e banco SQLite em memória
│   ├── graphs.py                  # Queries SQL + lógica de plotagem (Matplotlib)
│   └── ai_analyst.py              # Configuração do agente Agno + Gemini
├── Dockerfile
├── docker-compose.yml             # Base, neutra de SO
├── docker-compose.linux.yml       # Override: Linux nativo
├── docker-compose.wslg.yml        # Override: Windows 11 / WSLg
├── docker-compose.dev.yml         # Override: bind mounts para desenvolvimento
├── .dockerignore
├── .env.example                   # Template — copie para .env
├── requirements.txt
├── README.md
└── README_DOCKER.md
```

---

### Como rodar

**Pré-requisitos:** Python 3.10+ e uma [chave de API do Google AI Studio](https://aistudio.google.com/) (tier gratuito disponível).

```bash
# 1. Clone o repositório
git clone https://github.com/pedrodechichiribeiro/analyst_data_intern_challenge
cd analyst_data_intern_challenge

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure a chave da API
# Crie um arquivo .env na raiz com o conteúdo:
GOOGLE_API_KEY=sua_chave_aqui_AIza...

# 5. Rode
python src/main.py
```

**Via Docker:** veja o `README_DOCKER.md` para instruções de execução com GUI via X11 forwarding.

---

### Stack

Python · CustomTkinter · Matplotlib · Pandas · SQLite · Agno · Google Gemini 2.5 Flash · python-dotenv

---

— Pedro
