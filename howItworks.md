# How It Works: GenAi-main Project

This document describes every file in the GenAi-main folder, including their purpose and key functions/classes.

## Core Files

### `README.md`
- **Purpose**: Project documentation and overview.
- **Content**: Describes the multi-agent system for business memo generation, installation, usage, architecture, and limitations.

### `business_memo_system.py`
- **Purpose**: Main CLI script for running the full multi-agent pipeline.
- **Key Functions**:
  - `store_feedback(topic, edit_request)`: Stores style edit requests in `feedback_memory.csv`.
  - `is_missing_info_request(edit_request)`: Detects if edit request is for missing information (triggers re-retrieval).
  - `merge_datapoints(old_points, new_points, limit)`: Merges and deduplicates data points.
  - `get_used_sources(points)`: Extracts used case IDs from data points.
  - `BusinessMemoSystem` class:
    - `__init__()`: Initializes agents and logger.
    - `run(topic, max_revision_cycles)`: Orchestrates the full workflow: retrieval, drafting, approval, revisions, logging.

### `streamlit_app.py`
- **Purpose**: Web interface using Streamlit for interactive memo generation.
- **Key Functions**:
  - `is_missing_info_request(edit_request)`: Same as in CLI.
  - `merge_datapoints(old_points, new_points, limit)`: Same as in CLI.
  - `get_used_sources(points)`: Same as in CLI.
  - `store_style_feedback_csv(topic, edit_request)`: Stores style feedback in CSV.
  - `get_revision_cycles()`: Calculates revision count.
  - `set_busy(flag)`: Manages UI busy state.
  - `reset_run(new_topic)`: Resets session state.
  - `run_draft(edit_request)`: Generates a draft using DraftingAgent.
  - Main app logic: Handles UI events, agent calls, feedback logging.

## Agent Files

### `analyst_agent.py`
- **Purpose**: Retrieves relevant data points from the dataset.
- **Key Functions**:
  - `AnalystAgent` class:
    - `__init__(csv_path, top_k)`: Loads CSV rows.
    - `_load_rows()`: Parses CSV into list of dicts.
    - `_tokenize(text)`: Tokenizes text for similarity.
    - `run(topic, exclude_sources)`: Retrieves top-matching data points, excluding used sources.

### `drafting_agent.py`
- **Purpose**: Generates business memo drafts using LLM.
- **Key Functions**:
  - `DraftingAgent` class:
    - `__init__(model_name)`: Initializes LLM and preference store.
    - `_format_data_points(data_points)`: Formats data points as bullet list.
    - `_length_instruction(edit_request)`: Determines length based on request.
    - `_preference_instructions(edit_request)`: Injects learned preferences.
    - `_postprocess(email_text)`: Cleans LLM output (removes sources, extra lines).
    - `run(draft_input)`: Generates memo draft.

### `approval_agent.py`
- **Purpose**: Handles human approval in CLI mode.
- **Key Functions**:
  - `ApprovalAgent` class:
    - `run(draft)`: Prints draft and prompts for approve/edit.

## Core Modules

### `models.py`
- **Purpose**: Defines data structures using dataclasses.
- **Classes**:
  - `DataPoint`: Text and optional source.
  - `AnalystOutput`: Topic and list of DataPoints.
  - `DraftInput`: Topic, DataPoints, edit_request, version, grounded.
  - `DraftOutput`: Subject, body, version.
  - `ApprovalOutput`: Decision and optional edit_request.
  - `ApprovalDecision`: Literal type for decisions.

### `llm_client.py`
- **Purpose**: Interface to local LLM via Ollama.
- **Key Functions**:
  - `LocalLLM` class:
    - `__init__(model_name)`: Sets model.
    - `generate_email(prompt)`: Runs Ollama subprocess.
    - `run(prompt)`: Generic LLM call.

### `database.py`
- **Purpose**: SQLite database utilities.
- **Key Functions**:
  - `get_connection()`: Opens DB connection.
  - `init_db()`: Creates tables for evaluation_log and feedback_log.

## Logging and Evaluation

### `evaluation_logger.py`
- **Purpose**: Logs evaluation data to CSV.
- **Key Functions**:
  - `EvaluationLogger` class:
    - `__init__(filepath)`: Sets CSV path.
    - `log(topic, revision_cycles, final_decision, grounded)`: Appends to CSV.

### `evaluation_logger_sql.py`
- **Purpose**: Logs evaluation data to SQLite (alternative to CSV).
- **Key Functions**:
  - `EvaluationLoggerSQL` class:
    - `log(topic, revision_cycles, final_decision)`: Inserts into evaluation_log table.

### `feedback_logger.py`
- **Purpose**: Logs user feedback to SQLite.
- **Key Functions**:
  - `FeedbackLoggerSQL` class:
    - `log_feedback(topic, revision_cycles, rating, feedback_text)`: Inserts into feedback_log table.

### `analyze_evaluation.py`
- **Purpose**: Analyzes evaluation logs.
- **Key Functions**:
  - `load_evaluation_log(filepath)`: Loads CSV into list of dicts.
  - `main()`: Computes approval rate, average revisions, per-topic stats.

## Data Stores and Preferences

### `preference_store.py`
- **Purpose**: Extracts global preferences from feedback logs.
- **Key Functions**:
  - `PreferenceStore` class:
    - `_load_rows()`: Fetches feedback from SQLite.
    - `get_global_preferences()`: Analyzes feedback for preferences (short/long, professional).

### `feedback_store.py`
- **Purpose**: CLI helper for collecting and logging feedback.
- **Key Functions**:
  - `FeedbackStore` class:
    - `__init__()`: Initializes logger.
    - `collect_and_save(topic, revision_cycles)`: Prompts for rating/text, logs to DB.

### `business_memo_cases.csv`
- **Purpose**: Dataset of example memo cases with metadata and gold data points.
- **Columns**: case_id, topic, department, year, industry, region, currency, audience, tone, evidence_pack, gold_data_points.
- **Content**: 222+ rows of business scenarios with KPIs.

### `feedback_memory.csv`
- **Purpose**: CSV for storing style feedback (created by system).
- **Columns**: topic, feedback_text, created_at.

## Test Files

### `test_analyst.py`
- **Purpose**: Simple test script for AnalystAgent.
- **Content**: Instantiates agent, runs on sample topic, prints results.

### `test_drafting.py`
- **Purpose**: Simplified test version of DraftingAgent.
- **Key Functions**:
  - `DraftingAgent` class (test version):
    - `__init__()`: Initializes LLM.
    - `run(draft_input)`: Generates basic memo draft.

## Other

### `.gitignore`
- **Purpose**: Specifies files to ignore in version control (logs, DB, cache).

### `memo_system.db`
- **Purpose**: SQLite database file (created at runtime, ignored in git).