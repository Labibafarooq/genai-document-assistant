# GenAI – Business Memo Emailing Crew

## Overview
This project implements a **multi-agent Generative AI system** designed to automatically produce **professional business memos**. Instead of relying on a single prompt, the system uses a **structured multi-agent workflow** to improve output quality and consistency.

The workflow is composed of three agents:

**Analyst Agent → Drafting Agent → Approval Agent**

This project was developed as an **academic project** with an emphasis on clarity, reproducibility, evaluation, and software structure.

---

## Project Goal
The main goal of this project is to **automate the creation of business memos** using Large Language Models (LLMs) while maintaining a clear structure and quality control.

The project aims to:
- Demonstrate how **multi-agent architectures** can improve text generation quality  
- Separate reasoning, drafting, and validation into independent agents  
- Log evaluations and feedback for later analysis  
- Provide both a **command-line interface** and a **web interface** for interaction  

---

## System Architecture
The system follows a sequential pipeline:

```
User Input / Case
        |
        v
   Analyst Agent
 (understands intent,
  constraints, tone)
        |
        v
  Drafting Agent
 (generates memo draft)
        |
        v
  Approval Agent
 (reviews, validates,
  or requests revision)
        |
        +--> Evaluation & Feedback Logs
```

Each agent has a specific role, making the system easier to understand, debug, and extend.

---

## Key Features
- **Multi-agent architecture** (Analyst, Drafting, Approval)
- **LLM integration** through a dedicated client (`llm_client.py`)
- **Streamlit web interface** for interactive usage
- **Evaluation and feedback logging** using CSV and SQLite
- **Example dataset** for memo generation and testing
- Clear separation between logic, data models, and logging

---

## Project Structure
- `business_memo_system.py` – main orchestration pipeline (CLI)
- `streamlit_app.py` – Streamlit web interface
- `analyst_agent.py` – analyzes user intent and constraints
- `drafting_agent.py` – generates memo drafts
- `approval_agent.py` – validates and approves drafts
- `llm_client.py` – interface to the language model
- `models.py` – shared data models
- `database.py` – database utilities
- `analyze_evaluation.py` – evaluation analysis script
- `business_memo_cases.csv` – example input cases

---

## Installation

### 1) Create a virtual environment
```bash
python -m venv .venv
```

Activate it:

**Windows (Git Bash)**
```bash
source .venv/Scripts/activate
```

**Linux / macOS**
```bash
source .venv/bin/activate
```

---

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Project

### Option 1 — Command Line Interface
```bash
python business_memo_system.py
```

This runs the complete pipeline, generates a business memo, and logs evaluation and feedback data.

---

### Option 2 — Streamlit Web Interface
```bash
streamlit run streamlit_app.py
```

This provides an interactive web interface for generating and reviewing memos.

---

📊 Evaluation

Each run is evaluated immediately after the human approval step to track performance, efficiency, and grounding quality over time.

🔁 Evaluation flow

business_memo_system.py
Captures the memo topic, number of revision cycles, final decision (approve, reject, max_cycles_reached), and whether the final memo was grounded in retrieved evidence.

evaluation_logger.py
Appends the evaluation record to evaluation_log.csv and can also persist it in SQLite (memo_system.db).

calculate_ges.py / run_ges.py
Recomputes and prints the Global Evaluation Score (GES) to show how the system evolves across runs.

🧾 Logged fields (per run)

timestamp – UTC time when the run finished

topic – memo subject requested by the user

revision_cycles – number of edit loops before approval or rejection

final_decision – approve / reject / max_cycles_reached / unknown

grounded – whether the final memo was supported by curated evidence

📈 Global Evaluation Score (GES)

The Global Evaluation Score summarizes system performance across multiple runs using three signals:

Approval rate
Share of runs that ended with an approved memo.

Average revisions
Mean number of revision cycles per run. Runs requiring more than three revisions are penalized to reflect operational friction.

Groundedness rate
Share of approved memos that were backed by retrieved evidence rather than unsupported content.

These components are combined with weights 0.5 / 0.3 / 0.2, balancing:

final decision quality,

efficiency of iteration,

and factual grounding.

Higher GES values indicate more approvals, fewer revisions, and stronger evidence support.

🧠 Why this evaluation makes sense

Approval rate reflects final human or business judgment — the system only succeeds when approval is granted.

Revision penalties highlight inefficiencies in drafting or analysis agents.

Groundedness reinforces the retrieval-first design and discourages hallucinations.

Limiting the impact of revisions beyond three cycles mirrors real usage constraints in the CLI and Streamlit workflows.

Together, these signals encourage reliable approvals, faster iteration, and evidence-backed content.

🔍 How to analyze results

python run_ges.py – quick snapshot of the latest evaluation metrics

python analyze_evaluation.py – deeper analysis (per-topic averages, approval counts, trends)

evaluation_log.csv can also be loaded into notebooks or BI tools for custom analysis

This setup supports both quantitative tracking (GES) and qualitative review (per-run logs and feedback).

✅ Quality Assurance

Before pushing changes, run the checks below to ensure the evaluation pipeline remains healthy:

# Run unit tests (evaluation and scoring logic)
pytest

# Recompute the latest evaluation metrics
python run_ges.py



## Limitations
- Output quality depends on the underlying language model  
- No automatic factual verification is performed  
- Evaluation metrics are basic and intended for experimentation  

---

## Reproducibility & Submission Notes
- Generated artifacts (logs, databases, cache files) are excluded from version control  
- The repository is designed to be easy to clone and run by evaluators  
- This repository represents the **final submission version** of the project  

---


