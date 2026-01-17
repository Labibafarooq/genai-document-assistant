🚀 GenAI – Business Memo Emailing Crew

Multi-agent Generative AI system for automated professional business memo generation

🧠 Overview

This project implements a multi-agent Generative AI system that automatically produces professional business memos.

Instead of relying on a single prompt, the system uses a structured multi-agent workflow to improve:

output quality

consistency

validation and control

🔗 Agent Pipeline

Analyst Agent → Drafting Agent → Approval Agent

This project was developed as an academic project, with a strong focus on:

clarity

reproducibility

evaluation

clean software design

🎯 Project Objectives

The goal of this project is to automate business memo creation using Large Language Models (LLMs) while maintaining strict structure and quality control.

The system is designed to:

Demonstrate how multi-agent architectures improve text generation

Separate reasoning, drafting, and validation

Log evaluations and feedback for analysis

Support both CLI and web-based interaction

🏗️ System Architecture

The system follows a sequential and interpretable pipeline:

User Input / Case
        |
        v
   Analyst Agent
 (intent, constraints,
  tone understanding)
        |
        v
  Drafting Agent
 (memo generation)
        |
        v
  Approval Agent
 (review, validation,
  revision request)
        |
        +--> Evaluation & Feedback Logs


Each agent has a single responsibility, making the system:

easier to debug

easier to extend

easier to evaluate

✨ Key Features

🤖 Multi-agent architecture (Analyst / Drafting / Approval)

🔌 LLM abstraction layer (llm_client.py)

🌐 Streamlit web interface

📊 Evaluation & feedback logging (CSV + SQLite)

🧪 Example dataset for testing and demos

🧱 Clean separation of logic, models, and persistence

📁 Project Structure
.
├── business_memo_system.py   # CLI orchestration pipeline
├── streamlit_app.py          # Web interface (Streamlit)
├── analyst_agent.py          # Intent & constraint analysis
├── drafting_agent.py         # Memo generation
├── approval_agent.py         # Review & validation
├── llm_client.py             # LLM interface
├── models.py                 # Shared data models
├── database.py               # Database utilities
├── evaluation_logger.py      # Evaluation logging
├── calculate_ges.py          # Metric computation
├── analyze_evaluation.py     # Evaluation analysis
├── business_memo_cases.csv   # Example input cases

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
🖥️ Command Line Interface
python business_memo_system.py


Runs the full pipeline, generates a memo, and logs evaluation data.

🌐 Streamlit Web Interface
streamlit run streamlit_app.py


Launches an interactive web UI for generating and reviewing memos.

📊 Evaluation

Each run is evaluated immediately after human approval to track performance, efficiency, and factual grounding.

🔁 Evaluation Workflow

business_memo_system.py
Captures:

memo topic

revision cycles

final decision (approve, reject, max_cycles_reached)

grounding status

evaluation_logger.py
Logs each run to:

evaluation_log.csv

memo_system.db (SQLite)

calculate_ges.py / run_ges.py
Computes and displays the Global Evaluation Score (GES).

🧾 Logged Fields (Per Run)
Field	Description
timestamp	UTC completion time
topic	Requested memo subject
revision_cycles	Number of edit loops
final_decision	approve / reject / max_cycles_reached
grounded	Evidence-backed or not
📈 Global Evaluation Score (GES)

GES summarizes system performance using three signals:

Approval Rate
Share of runs ending in approval

Average Revisions
Mean number of revision cycles
(penalized when exceeding 3 cycles)

Groundedness Rate
Share of approved memos supported by retrieved evidence

Weights: 0.5 / 0.3 / 0.2

➡️ Higher scores mean:

more approvals

fewer revisions

better grounding

🧠 Why This Evaluation Works

Approval reflects final human judgment

Revision penalties expose inefficiencies

Groundedness discourages hallucinations

Revision limits match real CLI / Streamlit usage

This incentivizes quality, speed, and factual correctness.

🔍 Analyze Results
python run_ges.py


Quick metrics snapshot

python analyze_evaluation.py


Detailed analysis (per-topic stats, trends)

You can also load evaluation_log.csv into notebooks or BI tools.

✅ Quality Assurance

Before pushing changes, validate the pipeline:

pytest
python run_ges.py


These checks guard against scoring regressions and data corruption.

⚠️ Limitations

Output quality depends on the underlying LLM

No automatic factual verification

Metrics are experimental and research-oriented

📦 Reproducibility & Submission

Generated logs and databases are excluded from version control

Repository is easy to clone and run for evaluators

This represents the final submission version of the project
