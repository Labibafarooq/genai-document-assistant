🧠 GenAI – Business Memo Emailing Crew
Overview

This project implements a multi-agent Generative AI system designed to automatically produce professional business memos.
Instead of relying on a single prompt, the system uses a structured multi-agent workflow to improve output quality, consistency, and control.

The workflow is composed of three specialized agents:

Analyst Agent → Drafting Agent → Approval Agent

This project was developed as an academic project, with a strong focus on clarity, reproducibility, evaluation, and clean software structure.

🎯 Project Goal

The goal of this project is to automate the creation of business memos using Large Language Models (LLMs) while enforcing structure and quality control.

The system aims to:

Demonstrate how multi-agent architectures improve text generation quality

Separate reasoning, drafting, and validation into independent agents

Log evaluations and feedback for later analysis

Provide both a command-line interface and a web interface

🏗️ System Architecture

The system follows a sequential and interpretable pipeline:
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

Each agent has a clearly defined responsibility, making the system easier to understand, debug, and extend.

✨ Key Features

Multi-agent architecture (Analyst, Drafting, Approval)

LLM integration through a dedicated client (llm_client.py)

Streamlit web interface for interactive usage

Evaluation and feedback logging using CSV and SQLite

Example dataset for memo generation and testing

Clear separation between logic, data models, and logging

📁 Project Structure

business_memo_system.py – main orchestration pipeline (CLI)

streamlit_app.py – Streamlit web interface

analyst_agent.py – analyzes user intent and constraints

drafting_agent.py – generates memo drafts

approval_agent.py – validates and approves drafts

llm_client.py – interface to the language model

models.py – shared data models

database.py – database utilities

evaluation_logger.py – logs evaluation data

calculate_ges.py – computes evaluation metrics

analyze_evaluation.py – evaluation analysis script

business_memo_cases.csv – example input cases

⚙️ Installation
1️⃣ Create a virtual environment
python -m venv .venv

Activate it:

Windows (Git Bash)
source .venv/Scripts/activate
Linux / macOS
source .venv/bin/activate
2️⃣ Install dependencies
pip install -r requirements.txt

▶️ Running the Project
Option 1 — Command Line Interface
python business_memo_system.py
Runs the full pipeline, generates a memo, and logs evaluation and feedback data.

Option 2 — Streamlit Web Interface
streamlit run streamlit_app.py
Launches an interactive web interface for generating and reviewing memos.

📊 Evaluation

Each run is evaluated immediately after the human approval step to track performance, efficiency, and grounding quality over time.

🔁 Evaluation Flow

business_memo_system.py
Captures the memo topic, number of revision cycles, final decision (approve, reject, max_cycles_reached), and whether the final memo was grounded in retrieved evidence.

evaluation_logger.py
Appends the evaluation record to evaluation_log.csv and can also persist it in SQLite (memo_system.db).

calculate_ges.py / run_ges.py
Computes and prints the Global Evaluation Score (GES) to track system performance across runs.

🧾 Logged Fields (per run)

timestamp – UTC time when the run finished

topic – memo subject requested by the user

revision_cycles – number of edit loops before approval or rejection

final_decision – approve / reject / max_cycles_reached / unknown

grounded – whether the final memo was supported by curated evidence

📈 Global Evaluation Score (GES)

The Global Evaluation Score summarizes performance across multiple runs using three signals:

Approval rate – proportion of runs that ended with approval

Average revisions – mean number of revision cycles per run (penalized when exceeding three cycles)

Groundedness rate – proportion of approved memos backed by retrieved evidence

These components are combined using weights 0.5 / 0.3 / 0.2, balancing:

final decision quality,

efficiency of iteration,

and factual grounding.

Higher scores indicate more approvals, fewer revisions, and stronger evidence support.

🧠 Why This Evaluation Makes Sense

Approval rate reflects final human or business judgment

Revision penalties highlight inefficiencies in drafting or analysis

Groundedness discourages hallucinations and promotes retrieval-based reasoning

Revision limits mirror real usage constraints in CLI and Streamlit workflows

Together, these signals encourage reliable approvals, fast iteration, and evidence-backed content.

🔍 How to Analyze Results

python run_ges.py – quick snapshot of the latest evaluation metrics

python analyze_evaluation.py – deeper analysis (per-topic averages, approval counts, trends)

evaluation_log.csv can be loaded into notebooks or BI tools for custom analysis

This setup supports both quantitative tracking (metrics) and qualitative review (logs and feedback).

✅ Quality Assurance

Before pushing changes, run the following checks to ensure the pipeline remains healthy:
# Run unit tests (evaluation and scoring logic)
pytest

# Recompute the latest evaluation metrics
python run_ges.py

⚠️ Limitations

Output quality depends on the underlying language model

No automatic factual verification is performed

Evaluation metrics are intentionally simple and experimental

📦 Reproducibility & Submission Notes

Generated artifacts (logs, databases, cache files) are excluded from version control

The repository is designed to be easy to clone and run by evaluators

This repository represents the final submission version of the project
