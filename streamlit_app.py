import re
import os
import csv
from datetime import datetime, timezone

import streamlit as st

from analyst_agent import AnalystAgent
from drafting_agent import DraftingAgent
from models import DraftInput, DataPoint

from database import init_db
from feedback_logger import FeedbackLoggerSQL
from preference_store import PreferenceStore

# -----------------------------
# Init DB (SQLite)
# -----------------------------
init_db()

# -----------------------------
# Local constants
# -----------------------------
FEEDBACK_FILE = "feedback_memory.csv"

# -----------------------------
# Helpers (UI-safe)
# -----------------------------
def is_missing_info_request(edit_request: str | None) -> bool:
    if not edit_request:
        return False
    t = edit_request.lower().strip()
    patterns = [
        r"\bmissing\b",
        r"\badd(itional)?\b",
        r"\bmore info\b",
        r"\bmore details\b",
        r"\bmore information\b",
        r"\bneed more\b",
        r"\bi need more\b",
        r"\bincomplete\b",
        r"\bnot enough\b",
        r"\bexpand\b",
        r"\binclude all\b",
        r"\bdata\b",
        r"\bnumbers\b",
        r"\bkpi(s)?\b",
        r"\bmetrics\b",
        r"\bprovide\b.*\bdetails\b",
        r"\badditional\b.*\binformation\b",
    ]
    return any(re.search(p, t) for p in patterns)


def merge_datapoints(old_points: list[DataPoint], new_points: list[DataPoint], limit: int = 16) -> list[DataPoint]:
    seen = set()
    merged: list[DataPoint] = []
    for dp in old_points + new_points:
        key = (dp.text.strip().lower(), (dp.source or "").strip().lower())
        if key in seen:
            continue
        seen.add(key)
        merged.append(dp)
    return merged[:limit]


def get_used_sources(points: list[DataPoint]) -> set[str]:
    return {dp.source for dp in points if dp.source}


def store_style_feedback_csv(topic: str, edit_request: str) -> None:
    """Store human style edits into feedback_memory.csv (topic, feedback_text, created_at)."""
    if not edit_request:
        return
    file_exists = os.path.exists(FEEDBACK_FILE)
    with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow(["topic", "feedback_text", "created_at"])
        w.writerow([topic, edit_request, datetime.now(timezone.utc).isoformat()])


def get_revision_cycles() -> int:
    # v1 => 0 edits, v2 => 1 edit, ...
    return max(0, st.session_state.version - 1)


def set_busy(flag: bool) -> None:
    st.session_state.is_busy = flag


# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(page_title="Business Memo Emailing Crew", layout="wide")

st.sidebar.subheader("Learned preferences")
st.sidebar.json(PreferenceStore().get_global_preferences())

st.title("Business Memo Emailing Crew")
st.caption("Analyst → Drafting → Human-in-the-loop approval (Streamlit UI)")

# Init agents (kept in session for speed)
if "analyst" not in st.session_state:
    st.session_state.analyst = AnalystAgent()
if "drafter" not in st.session_state:
    st.session_state.drafter = DraftingAgent()

# Session state for workflow
defaults = {
    "topic": "",
    "grounded": False,
    "data_points": [],
    "version": 0,
    "current_draft": "",
    "approved": False,
    "history": [],       # list of dicts: {version, edit_request, draft}
    "is_busy": False,    # disable buttons while generating
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def reset_run(new_topic: str):
    st.session_state.topic = new_topic
    st.session_state.grounded = False
    st.session_state.data_points = []
    st.session_state.version = 0
    st.session_state.current_draft = ""
    st.session_state.approved = False
    st.session_state.history = []
    st.session_state.is_busy = False


def run_draft(edit_request: str | None):
    st.session_state.version += 1

    draft_input = DraftInput(
        topic=st.session_state.topic,
        data_points=st.session_state.data_points,
        edit_request=edit_request,
        version=st.session_state.version,
        grounded=bool(st.session_state.data_points),
    )

    draft_output = st.session_state.drafter.run(draft_input)
    st.session_state.current_draft = draft_output.body

    st.session_state.history.append({
        "version": st.session_state.version,
        "edit_request": edit_request,
        "draft": draft_output.body,
    })


left, right = st.columns([1.1, 1.4], gap="large")

with left:
    st.subheader("1) Topic")

    topic_input = st.text_input(
        "Enter memo topic",
        value=st.session_state.topic,
        placeholder='e.g., "sales revenue from 2016"',
        disabled=st.session_state.is_busy,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        generate_clicked = st.button(
            "Generate draft (v1)",
            type="primary",
            use_container_width=True,
            disabled=st.session_state.is_busy,
        )
    with col_b:
        reset_clicked = st.button(
            "Reset",
            use_container_width=True,
            disabled=st.session_state.is_busy,
        )

    if reset_clicked:
        reset_run(topic_input.strip())
        st.rerun()

    st.divider()
    st.subheader("2) Human decision")

    approve_clicked = st.button(
        "Approve ✅",
        disabled=(not st.session_state.current_draft) or st.session_state.is_busy,
        use_container_width=True,
    )

    with st.expander("Request edit ✏️", expanded=False):
        edit_text = st.text_area(
            "Edit request",
            placeholder="e.g., Make it shorter. / Use a more formal tone. / Add missing KPIs.",
            height=110,
            disabled=st.session_state.is_busy,
        )
        submit_edit = st.button(
            "Submit edit request",
            disabled=(not st.session_state.current_draft) or st.session_state.is_busy,
            use_container_width=True,
        )

    st.divider()
    st.subheader("3) Feedback (after approval)")

    if st.session_state.approved:
        rating = st.slider("Rate this memo (1–5)", 1, 5, 4, disabled=st.session_state.is_busy)
        fb_text = st.text_area(
            "Optional feedback (tone / length / clarity)",
            placeholder="e.g., Too long, make it more formal, improve action items...",
            disabled=st.session_state.is_busy,
        )

        save_feedback = st.button(
            "Save feedback ⭐",
            use_container_width=True,
            disabled=st.session_state.is_busy,
        )

        if save_feedback:
            logger = FeedbackLoggerSQL()
            logger.log_feedback(
                topic=st.session_state.topic,
                revision_cycles=get_revision_cycles(),
                rating_1_to_5=rating,
                feedback_text=(fb_text.strip() or None),
            )
            st.success("✅ Feedback saved into memo_system.db → feedback_log.")
    else:
        st.info("Approve the memo first to leave feedback.")

with right:
    st.subheader("Draft output")

    if st.session_state.current_draft:
        st.text_area(
            "Memo (what you would send)",
            value=st.session_state.current_draft,
            height=420,
        )
    else:
        st.info("Generate a draft to see the memo here.")

    # Optional: show internal evidence, but clearly labeled as NOT part of memo
    with st.expander("Internal evidence (NOT included in the memo)", expanded=False):
        if st.session_state.data_points:
            for dp in st.session_state.data_points:
                if dp.source:
                    st.write(f"- {dp.text}  \n  _(case: {dp.source})_")
                else:
                    st.write(f"- {dp.text}")
        else:
            st.write("No evidence loaded yet.")

    with st.expander("Version history", expanded=False):
        if st.session_state.history:
            for item in reversed(st.session_state.history):
                st.markdown(f"**v{item['version']}** — Edit request: `{item['edit_request'] or 'None'}`")
                st.text(item["draft"][:900] + ("..." if len(item["draft"]) > 900 else ""))
                st.markdown("---")
        else:
            st.write("No history yet.")


# -----------------------------
# Actions
# -----------------------------
if generate_clicked:
    new_topic = topic_input.strip()
    if not new_topic:
        st.warning("Please enter a topic first.")
    else:
        if st.session_state.topic != new_topic:
            reset_run(new_topic)

        set_busy(True)
        try:
            with st.spinner("AnalystAgent: retrieving evidence..."):
                analyst_out = st.session_state.analyst.run(st.session_state.topic)
                st.session_state.data_points = analyst_out.data_points
                st.session_state.grounded = bool(st.session_state.data_points)

            with st.spinner("DraftingAgent: writing memo..."):
                run_draft(edit_request=None)

        finally:
            set_busy(False)

        st.rerun()


if submit_edit:
    req = (edit_text or "").strip()
    if not req:
        req = "Please improve clarity and conciseness."

    set_busy(True)
    try:
        # If missing-info request: rerun retrieval and merge new evidence
        if is_missing_info_request(req):
            with st.spinner("Missing-info detected: retrieving additional evidence..."):
                used_sources = get_used_sources(st.session_state.data_points)
                query = f"{st.session_state.topic}. User request: {req}"
                analyst_out_2 = st.session_state.analyst.run(query, exclude_sources=used_sources)
                st.session_state.data_points = merge_datapoints(
                    st.session_state.data_points,
                    analyst_out_2.data_points,
                    limit=16
                )
        else:
            # Style edits get stored for your "memory" CSV
            store_style_feedback_csv(st.session_state.topic, req)

        with st.spinner("DraftingAgent: revising memo..."):
            run_draft(edit_request=req)

    finally:
        set_busy(False)

    st.rerun()


if approve_clicked:
    st.session_state.approved = True
    st.success("✅ Memo approved!")
