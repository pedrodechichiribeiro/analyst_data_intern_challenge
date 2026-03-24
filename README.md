# Dashboard de Análise de Dados com IA

Olá, sou **Pedro Dechichi Ribeiro**.

Esse projeto nasceu como solução para um desafio técnico de processo seletivo de estágio. Não passei, mas o que construí tinha substância suficiente para virar um projeto de portfólio real — então continuei desenvolvendo.

O resultado é um dashboard desktop de análise de tickets de suporte técnico, que combina SQL, visualização de dados e um agente de IA em nuvem para gerar relatórios executivos automaticamente.

---

## O que o projeto faz

A aplicação carrega dois datasets JSON com dados anonimizados de chamados de suporte, processa tudo via SQLite em memória, exibe 9 visualizações interativas e, ao clicar num botão, envia o contexto do gráfico ativo para o Google Gemini — que retorna uma análise com riscos, tendências e recomendações operacionais.

O fluxo completo é: dados brutos → SQL → gráfico → IA → insight.

---

## Visualizações disponíveis

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

## Agente de IA

Cada visualização carrega um `system_prompt` e um `data_context` específicos. Ao clicar em **"Generate Deep Analysis"**, esses dados são enviados para um agente [Agno](https://github.com/agno-agi/agno) configurado com o modelo **Gemini 2.5 Flash**, que atua como analista sênior de operações de suporte.

A análise roda em thread separada para não travar a interface.

---

## Estrutura do projeto

```
├── data/
│   ├── accounts_anonymized.json
│   └── support_cases_anonymized.json
├── src/
│   ├── main.py           # Interface e layout (CustomTkinter)
│   ├── data_manager.py   # Carga dos JSONs e banco SQLite em memória
│   ├── graphs.py         # Queries SQL + lógica de plotagem (Matplotlib)
│   └── ai_analyst.py     # Configuração do agente Agno + Gemini
├── .env                  # Chave da API (não versionado)
├── requirements.txt
└── README.md
```

---

## Como rodar

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

**Windows:** o repositório inclui um `run.bat` que automatiza os passos 2 a 5.

**Via Docker:** veja o `README_DOCKER.md` para instruções de execução com GUI via X11 forwarding.

---

## Stack

Python · CustomTkinter · Matplotlib · Pandas · SQLite · Agno · Google Gemini 2.5 Flash · python-dotenv

---

— Pedro
