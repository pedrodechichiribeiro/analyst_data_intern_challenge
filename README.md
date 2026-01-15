note: i've run this using Windows 11 and VSCode

# Summary

Hi! My name is **Pedro Dechichi Ribeiro**. I'm computer engineering student on the "Universidade Federal de Uberlândia" (UFU for short) in Brazil.

This repository is my submission for the "GlobalVision Systems & Data Intern Take Home". The goal was, given the anonymized datasets provided, utilize SQL and Python to produce insightful data visualizations that could produce meaningful support for business decisions. 

My solution was to create a responsive dashboard where the user would have acess for 9 different graphs and charts that i've judged had important takeaways from the displayed data. They are:

### 1 - Top Products by Ticket Number: 
- Clearly identifies the top 10 most common products on the datasets, ranking them on a bar-chart. Standard metric to understand the demand (or lack there of) of each available service by GlobalVision

### 2 - Severity Stack:
- Bar chart that displays the top 10 products severity distribution percentiles. It allows the user to quickly visualize the % of each severity category on the products, identifiying the most proportionally problematic ones. 

### 3 - Case Types:
- A pie chart that categorizes incoming tickets (e.g., Bugs, Questions, Feature Requests). It groups smaller categories into "Other" to keep the visual clean. This is vital for understanding the nature of the support load—whether teams are fixing defects or just answering training questions.

### 4 - Global Hotspots:
- A geographical bar chart displaying the top 10 countries by total case volume. This visualization helps Operations Managers identify where the bulk of the support load originates, which is crucial for staffing decisions regarding language support and time zone coverage.

### 5 - Ticket Density Analysis:
- Instead of just looking at total volume (which is biased towards countries with many customers), this horizontal bar chart calculates the "neediness" of a region by dividing total cases by the number of unique accounts. It highlights regions that generate a disproportionately high number of tickets per customer, signaling potential quality issues or a need for better localized training.

### 6 - Industry Struggles:
- Segments the support data by client market sector (e.g., Tech, Energy, Retail). This helps the Product Team identify if specific industries are struggling with the software more than others, potentially revealing gaps in compliance features or industry-specific workflows.

### 7 - Volume Over Time:
- A temporal line chart showing the weekly influx of new support cases. By smoothing the data into weekly averages, this graph filters out daily noise to reveal the true long-term trend—whether the support burden is growing, stabilizing, or shrinking—allowing for proactive staffing.

### 8 - Time to Resolution:
- A histogram that displays the distribution of how many days it takes to close a case. It helps visualize team efficiency and identify "long-tail" issues—outliers that take significantly longer than average to resolve—which often indicate complex, systematic problems.

### 9 - Backlog Growth:
- A dual-line area chart comparing the total number of cases opened versus cases closed over time. The diverging space between these lines visually represents the growing backlog. This is the most critical metric for resource planning, as a widening gap indicates the team is overwhelmed and cannot keep up with the incoming rate of work.

---

In an attempt to differentiate myself from other candidates, I've implemented a local AI agent for data analysis. The model used is **Gemma 3 4B (quantized)**. It strikes a balance between performance and accessibility: large enough to minimize hallucinations, yet small enough to run on widely available hardware. Please note that this acts more as a 'proof of concept' than a final implementation. Since I do not know the specifications of the device running this code, I could not fully optimize the model for speed or cohesion. It may run slowly on older machines, but it should work on any system meeting these minimum requirements:

- 8GB DDR4 RAM (16GB recommended, as the DB is loaded into memory)
- 3gb disk space (recommend SSD)
- Ryzen 3600G / Intel i5-8400

    **Note:** Even if the AI does not load, the graphs will still function normally as intended.

---

# SETTING IT UP:

## 0. Have python installed

## 1. Clone this repository 

- https://github.com/pedrodechichiribeiro/analyst_data_intern_challenge

## 2. Download Gemma 3:

- 2.1: Go to **"https://huggingface.co/unsloth/gemma-3-4b-it-GGUF/blob/main/gemma-3-4b-it-Q4_K_M.gguf"**
- 2.2: Download  the specific model **"gemma-3-4b-it-Q4_K_M.gguf"**
- 2.3: Place it on the **"models" folder**

**IMPORTANT!**: IT WONT WORK WITH ANY OTHER MODEL WITHOUT CODE CHANGES (on ai_analyst.py)

## 3. Run "setup.py"

This installs **"requirements.txt"** and **llama-cpp-python** without the need for a C++ compiler. Await for the installation to finish, it's only needed on the first time configuration

## 4. Run "python src/main.py"

You can select the graphs/charts options from the buttons on the top of the screen and generate AI insights by clicking on the button on the bottom right (wait some time if your device is older for generation). Enjoy the app!

---

# EXTRA INFO:

- 1. All SQL prompts are located in **"graphs.py"**, the SQL connection is estabilished on **"data_manager.py"**
- 2. This program utilizes the following third-party libraries: 

    - **CustomTkinter** (GUI and dashboard)
    - **Matplotlib** (graph and chart plotting)
    - **Pandas** (data analysis and manipulation) 
    - **Numby** (graph normalization) 
    - **llama-cpp-python** (AI agent implementation)
