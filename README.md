# README — GlobalVision Systems & Data Intern Take Home

Hi — I'm **Pedro Dechichi Ribeiro**. This repository contains my solution for the **GlobalVision Systems & Data Intern** take‑home challenge. I built a small local dashboard and analysis pipeline that uses Python + SQL to explore the provided anonymized Salesforce data, produce meaningful KPIs, and surface actionable business insights.

> I ran this on Windows 11. Keep that in mind if you use another OS — small platform differences (Tkinter, fonts) may appear.

---

## What the challenge asked for (brief)

The original challenge required that you:

1. Load and explore two datasets: `accounts_anonymized.json` and `support_cases_anonymized.json`.
2. Use Python and SQL to join and process the data and derive useful metrics (SQL should be used for this part).
3. Produce visualizations that explain those KPIs.
4. Explain key insights and propose two actionable recommendations.
5. Submit a Python script/notebook and a short video walkthrough (≤ 5 minutes).

This README adapts the repository to exactly match those instructions and explains how to run and review my submission.

---

## What I built (summary)

A responsive local dashboard that exposes **9 visualizations** I judged most valuable from the data. They are:

1. **Top Products by Ticket Number** — top 10 products by total cases (bar chart).
2. **Severity Stack** — top 10 products with stacked percentiles for severity levels.
3. **Case Types** — pie chart grouping minor categories into “Other” for clarity.
4. **Global Hotspots** — top 10 countries by case volume (geographic focus for staffing).
5. **Ticket Density Analysis** — cases per unique account (shows regions with high tickets per customer).
6. **Industry Struggles** — support volume segmented by client industry.
7. **Volume Over Time** — weekly new-case trend (smoothed to show long-term movement).
8. **Time to Resolution** — histogram of days-to-close (reveals long-tail cases).
9. **Backlog Growth** — opened vs closed cases over time (shows backlog divergence).

Each chart is accessible through the dashboard UI (top buttons) and designed to answer a concrete operational question.

---

## How this maps to the challenge parts

* **Part 1 — Data Exploration:** The `src/data_manager.py` loads and inspects the JSON files. The dashboard and helper scripts include simple EDA outputs (counts, null checks, sample rows).

* **Part 2 — Data Processing (SQL + Python):** All main SQL queries used to create the charts live in `src/graphs.py` and run against an in-memory SQLite instance created in `src/data_manager.py`. I used pandas + sqlite3 for ETL and SQL logic.

* **Part 3 — Visualizations:** Charts are produced with Matplotlib and rendered in the GUI built with CustomTkinter. The plotting code is in `src/graphs.py` and `src/plot_utils.py`.

* **Part 4 — Business Insights:** The dashboard includes an AI analysis button (bottom-right) that generates a short summary of insights. I also include a `REPORT.md` (or `INSIGHTS.md`) file in the repo that lists the key findings and two actionable recommendations derived from the data.

---

## Setup & run (quick)

Prerequisites:

* Python 3.10+ recommended. I tested with Python 3.14.2 on Windows 11. 
* **SETUP.PY DOES NOT WORK WITH PYTHON 3.14** (llama-cpp does not have a version that recent)
* *if using python v3.14 or higher install using **"pip install llama-cpp-python"** (will need a C++ compiler)
* Optional: an environment manager (venv, conda)

Steps:

1. Clone the repository:

```bash
git clone https://github.com/pedrodechichiribeiro/analyst_data_intern_challenge
cd analyst_data_intern_challenge
```

2. (Optional but recommended) Create a venv and activate it:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. Install dependencies:

* Ff you are running python 3.10 through 3.12:
```bash
python setup.py
```
This script installs the packages from `requirements.txt` and configures `llama-cpp-python` without requiring a local C++ compiler (first-time setup may take a few minutes).

* If you are running python 3.14 or higher get a C++ compiler, ignore setup.py and run:

```bash
pip install llama-cpp-python
pip install -r requirements.txt
```

4. (If you want the local AI assistant) Download the model and place it in `models/` (optional — the dashboard works without the AI agent):

* Model used: **Gemma 3 4B (quantized)** (https://huggingface.co/unsloth/gemma-3-4b-it-GGUF/blob/main/gemma-3-4b-it-Q4_K_M.gguf)
* Place file name `gemma-3-4b-it-Q4_K_M.gguf` into the `models/` directory. It will break if you use other models without changing the code in ai_analyst.py

> **Important:** The AI assistant is a proof of concept. If the model is not present, the app still functions and the visualizations are unchanged.

5. Run the app:

```bash
python src/main.py
```

Use the top buttons to switch between charts. Click the bottom-right button to generate an AI-assisted summary (if model available).

---

## Files of interest

* `src/main.py` — app entrypoint and UI layout.
* `src/data_manager.py` — loads JSON files, builds the in-memory SQLite DB, and prepares dataframes.
* `src/graphs.py` — SQL queries and plotting logic for each chart (primary SQL is here).
* `src/plot_utils.py` — plotting helpers and formatting.
* `requirements.txt` — Python dependencies.
* `models/` — optional folder to drop the Gemma model.
* `accounts_anonymized.json` and `support_cases_anonymized.json` — the two provided datasets (place them in the repo root or `data/` according to the script expectations).

---

## Minimum recommended hardware

The AI assistant is the heaviest optional component. Minimum recommended specs to run everything comfortably:

* **16 GB RAM** (8 GB _may_ work but will be slow if AI loads)
* **~3 GB disk** (SSD recommended)
* CPU roughly equivalent to Ryzen 3600G / Intel i5-8400 or newer.
* GPU recommended, specially with CUDA cores. Just makes generataing faster

My dev machine: Intel i5-14600KF, Radeon 9060 16GB, 32 GB DDR5 — I used that to test performance.

---

## Notes, caveats & small details

* The project favors clarity and reproducibility: SQL queries are intentionally explicit and placed together in `graphs.py` for review.
* The AI assistant is **optional** and only included as a differentiator; it’s not required to reproduce the visual insights.
* If you run into `Tkinter` problems on Linux, install `python3-tk` (e.g. `sudo apt-get install python3-tk` or distro equivalent).

---

## Quick reproduction commands

```bash
# install and run (assumes Python is present)
python setup.py
python src/main.py
```

If you prefer to run a single script that generates PNG exports of all charts (no GUI), see `src/export_charts.py` (it runs the same SQL queries and saves outputs in `outputs/`).

---

## Final thoughts

Thanks for taking a look! I tried to preserve useful implementation details while making the repository explicitly match the take‑home's requirements: Python + SQL processing, visualizations, and a concise set of business recommendations. Even if doesn't get me selected it was a rather fun quick side project.

— Pedro
