🧠 GenAI – Business Memo Emailing Crew
<p align="center"> <strong>Multi-Agent Generative AI system for automated professional business memos</strong> </p>
🔥 What is this?

A multi-agent Generative AI system that creates professional business memos using a controlled workflow instead of a single prompt.

Three agents. One pipeline. Human-in-the-loop approval.

Analyst  →  Drafting  →  Approval


Built as an academic + engineering project, with evaluation, logging, and reproducibility in mind.

🎯 Why it exists

Most GenAI demos stop at “it generated text”.
This project focuses on control, structure, and evaluation.

It shows how to:

break text generation into independent agents

keep humans in the loop

measure quality over time

avoid prompt spaghetti

🧩 Architecture (Simple & Clear)
User Input
   ↓
Analyst Agent
(intent, constraints, tone)
   ↓
Drafting Agent
(memo generation)
   ↓
Approval Agent
(approve / reject / revise)
   ↓
Evaluation + Logs


Each agent does one job only.

✨ Features
Feature	Description
🤖 Multi-Agent System	Analyst, Drafting, Approval agents
🔌 LLM Abstraction	Centralized LLM client
🌐 Web UI	Streamlit interface
📊 Evaluation	CSV + SQLite logging
🧪 Reproducible	Same inputs → same evaluation
🧱 Clean Design	Clear separation of concerns
📁 Project Layout
.
├── business_memo_system.py   # CLI pipeline
├── streamlit_app.py          # Web UI
├── analyst_agent.py          # Intent analysis
├── drafting_agent.py         # Memo generation
├── approval_agent.py         # Review & approval
├── llm_client.py             # LLM interface
├── evaluation_logger.py      # Logging
├── calculate_ges.py          # Metrics
├── analyze_evaluation.py     # Analysis
├── business_memo_cases.csv   # Example cases

⚙️ Setup
python -m venv .venv
source .venv/bin/activate   # or .venv/Scripts/activate on Windows
pip install -r requirements.txt

▶️ Run It
CLI
python business_memo_system.py

Web App
streamlit run streamlit_app.py

📊 Evaluation (The Important Part)

Every run is evaluated after human approval.

What gets logged
Field	Meaning
timestamp	Run completion time
topic	Requested memo topic
revision_cycles	Number of edits
final_decision	approve / reject / max_cycles_reached
grounded	Evidence-based or not
Global Evaluation Score (GES)

GES combines:

Approval rate

Revision efficiency

Groundedness

Higher score =
✔ more approvals
✔ fewer revisions
✔ better evidence usage

🔍 Analyze Performance
python run_ges.py

python analyze_evaluation.py


Use evaluation_log.csv for notebooks or BI tools.

✅ Quality Checks
pytest
python run_ges.py

⚠️ Limitations

Depends on underlying LLM quality

No automatic fact-checking

Metrics are experimental

📦 Notes

Logs and databases are excluded from Git

Designed to be easy to clone and evaluate

This repository represents the final project version
