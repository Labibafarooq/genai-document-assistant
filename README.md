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

Evaluation

Every run is evaluated immediately after the human approval step:

business_memo_system.py captures the topic, number of revision cycles, final decision (approve / reject / max_cycles_reached), and whether the final memo was grounded in retrieved evidence.

evaluation_logger.py appends this row to evaluation_log.csv (CSV) and can also persist it in SQLite (memo_system.db).

After logging, calculate_ges.py can recompute the Global Evaluation Score (GES) so you can see how the system is trending over time. The helper script run_ges.py prints the latest metrics with one command.

Logged fields (per run)

timestamp: UTC time the run finished

topic: memo subject the user requested

revision_cycles: number of edit loops completed before approval/rejection

final_decision: approve / reject / max_cycles_reached / unknown

grounded: True if at least one curated data point supported the final draft

Global Evaluation Score (GES)

To summarize multiple runs, we compute:

$$
\text{GES} =
0.5 \cdot \text{approval\_rate}
+ 0.3 \cdot \left(1 - \min\left(1, \frac{\text{avg\_revisions}}{3}\right)\right)
+ 0.2 \cdot \text{groundedness\_rate}
$$

Where:

Approval rate – share of runs that ended in approve.

- **Average revisions** – mean revision cycles per run; more than 3 cycles are penalized when the average exceeds three.



Groundedness rate – share of approved memos that were grounded in retrieved evidence.

This weighting (0.5 / 0.3 / 0.2) balances quality, efficiency, and factual support. Higher scores mean more approvals, fewer revisions, and better grounding.

Why this formula fits the project

Approval rate captures the final human/business judgment—the multi-agent loop only succeeds if the approval agent signs off.

The revision penalty translates operational friction: if drafts need many edits, the drafting or analyst agents need tuning.

Groundedness reinforces the retrieval-first design by rewarding memos backed by curated evidence instead of hallucinations.

Normalizing revisions at three cycles mirrors the guardrails in the CLI/Streamlit flows (which stop after ~3 rounds), so the metric reflects real usage limits.

Together, these signals incentivize improvements that matter most for a memo assistant: reliable approvals, fast iteration, and evidence-backed content.

How to analyze results

python run_ges.py – quick snapshot of the latest metrics.

python analyze_evaluation.py – richer statistics (per-topic averages, approval counts, etc.).

You can also load evaluation_log.csv into your own BI or notebook workflows for deeper dives.

These tools support both quantitative tracking (GES) and qualitative review (per-run logs, feedback).

Quality Assurance ✅

Before pushing changes, run the quick validation suite below to confirm the pipeline is still healthy:
# 1. Unit tests (calculate GES edge cases)
pytest

# 2. Recompute the latest evaluation metrics
python run_ges.py


The pytest suite focuses on calculate_ges edge cases (empty logs, all approvals, mixed outcomes) and guards against regressions in the scoring logic.

run_ges.py consumes the current evaluation_log.csv and echoes the aggregate metrics that the CLI prints after each approval, which doubles as a sanity check for CSV integrity.

If you change the human-in-the-loop flow (business_memo_system.py or streamlit_app.py), also run those manually because they require interactive approval input that automated tests can’t cover.


Parts of this repository were authored with the help of an AI pair-programming assistant (for example, composing documentation, drafting helper scripts, and generating test data for evaluation_log.csv).

All AI-generated changes were reviewed, edited, and validated with the tests above to ensure correctness and maintain project style.

Whenever you iterate further, continue logging how AI contributes so downstream reviewers understand which components were machine-assisted.

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


