# 🧠 GenAI Business Memo Crew

<p align="center">
  <b>Multi-agent Generative AI system for controlled business memo generation</b>
</p>

<p align="center">
  Analyst → Drafting → Approval · Human-in-the-loop · Evaluation-driven
</p>

---

## ⚡ One-line summary
A **multi-agent GenAI pipeline** that generates professional business memos with **human approval**, **revision control**, and **measurable quality metrics**.

---

## 🧩 How it works

User
↓
Analyst Agent (intent & constraints)
↓
Drafting Agent (memo generation)
↓
Approval Agent (approve / reject / revise)
↓
Evaluation + Logs


Each agent has **one responsibility**.  
No prompt soup. No hidden logic.

---

## ✨ Why this project matters

Most GenAI demos stop at *“it generated text”*.

This project focuses on:
- **control** instead of raw generation
- **human decision points**
- **measurable quality over time**
- **clean system design**

---

## 🛠️ Features

- 🤖 Multi-agent architecture  
- 👤 Human-in-the-loop approval  
- 📊 Automatic evaluation & scoring  
- 🌐 Streamlit web interface  
- 📁 CSV + SQLite logging  
- 🧪 Reproducible experiments  

---

## 📁 Repository Layout

business_memo_system.py # CLI pipeline
streamlit_app.py # Web UI
analyst_agent.py # Intent analysis
drafting_agent.py # Memo generation
approval_agent.py # Review & approval
llm_client.py # LLM abstraction
evaluation_logger.py # Run logging
calculate_ges.py # Metrics
analyze_evaluation.py # Analysis


---

## ▶️ Run it

```bash
python business_memo_system.py

or

streamlit run streamlit_app.py
📊 Evaluation (core idea)

Every run is evaluated after approval.

What’s tracked

topic

revision count

final decision

grounding (evidence-based or not)

Global Evaluation Score (GES) reflects:

approval success

iteration efficiency

factual grounding

Higher score = better system behavior.

🔍 Analyze results
python run_ges.py
python analyze_evaluation.py


Use evaluation_log.csv for notebooks or BI tools.

⚠️ Limits

Depends on LLM quality

No automatic fact-checking

Metrics are experimental

📌 Notes

Logs & databases excluded from Git

Easy to clone & evaluate

Final academic project version


---

### Why **this** one actually looks good
- Short sections  
- No walls of text  
- Clear hierarchy  
- White space  
- Reads in **30 seconds**  

If you want to go **one level higher** (actually 🔥):
- add **GitHub badges**
- add **one PNG architecture diagram**
- add **“Why multi-agent > single prompt”**

Say **which one** and I’ll do it cleanly.

