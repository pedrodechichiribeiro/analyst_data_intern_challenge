# README — AI-Powered Data Analysis Dashboard

Hi — I'm **Pedro Dechichi Ribeiro**. This repository contains a data analysis dashboard built with Python, SQL, and **Agno**. It processes anonymized support ticket data to produce meaningful KPIs, visualizations, and actionable business insights using cloud-based AI.

> **Note:** This project was originally a take-home challenge solution. It has since been updated to serve as a proof-of-concept for using **Agno** and **Google Gemini** for automated data reporting.

---

## Project Overview

This tool is designed to:

1. **Ingest Data:** Load and explore anonymized JSON datasets (`accounts` and `support_cases`).
2. **Process via SQL:** Use an in-memory SQLite database to join tables and derive complex metrics.
3. **Visualize:** Render interactive charts using **CustomTkinter** and Matplotlib.
4. **Analyze with AI:** Use an **Agno Agent** powered by **Google Gemini** to generate executive summaries and strategic recommendations based on the visualized data.

---

## Features

### Visualizations

The dashboard exposes **9 key visualizations** accessible via the top navigation bar:

1. **Top Products by Ticket Number** — Volume analysis by product hardware/software.
2. **Severity Stack** — Severity level distribution per product.
3. **Case Types** — Categorical distribution of support requests.
4. **Global Hotspots** — Geographic heat map of case volumes.
5. **Ticket Density Analysis** — Average tickets per unique account by region.
6. **Industry Struggles** — Support volume segmented by client market sector.
7. **Volume Over Time** — Weekly new-case trends (smoothed).
8. **Time to Resolution** — Histogram of days-to-close.
9. **Backlog Growth** — Opened vs. Closed case rates over time.

### AI Analyst (Agno + Gemini)

Clicking the "Generate Deep Analysis" button triggers a cloud-based agent. The system sends the specific data context of the currently visible chart to Google Gemini, which acts as a Senior Data Scientist to return actionable insights, trend warnings, and operational advice.

---

## Setup & Run

### Prerequisites

* **Python 3.10+** (Tested on Windows 11).
* A **Google AI Studio API Key** (Free tier available).

### Installation

0. **If on Windows**

Update API key and name of the file on **.env**
Then double click on run.bat and everything will be done automatically, skipping the steps 1 through 5.
If it does not work then please do it step by step like below:

1. **Clone the repository:**
```bash
git clone https://github.com/pedrodechichiribeiro/analyst_data_intern_challenge
cd analyst_data_intern_challenge

```


2. **Create and activate a virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Configure Environment Variables:**
* Create a file named `.env` in the root directory.
* Add your Google API key (Get one [here](https://aistudio.google.com/)):


```ini
GOOGLE_API_KEY=your_api_key_starts_with_AIza...

```


5. **Run the App:**
```bash
python src/main.py

```



---

## Files of Interest

* `src/main.py` — Application entry point and UI layout.
* `src/ai_analyst.py` — **Agno Agent configuration.** Handles the connection to Google Gemini and prompts the model with context-aware instructions.
* `src/data_manager.py` — Loads JSON files and manages the SQLite in-memory database.
* `src/graphs.py` — Contains the raw SQL queries and Matplotlib plotting logic.
* `src/plot_utils.py` — Helper functions for graph styling.
* `requirements.txt` — Project dependencies (Agno, CustomTkinter, Matplotlib, etc.).

---

## Hardware Requirements

Unlike the previous version of this project which ran a 4GB LLM locally, this version offloads intelligence to the cloud.

* **RAM:** 4GB+ is sufficient.
* **Internet:** Active connection required for AI features.
* **Disk:** Minimal (< 200MB).

---

## Notes & Caveats

* **API Usage:** The AI features use the Google Gemini API. Ensure you are within the free tier limits or have billing configured if you plan to spam requests.
* **Privacy:** Data snippets (numbers and text labels) are sent to the Google API for analysis. Do not use this configuration with strictly confidential PII without reviewing Google's data privacy policies for the API.
* **Linux Users:** If you encounter `Tkinter` errors, ensure `python3-tk` is installed via your package manager.

---

## Final Thoughts

This project demonstrates how easily modern Agentic frameworks like **Agno** can be integrated into legacy desktop applications to provide "Intelligence as a Service," replacing complex local setups with lightweight API calls.

— Pedro