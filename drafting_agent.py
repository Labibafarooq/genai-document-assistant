from typing import List, Optional
import re
from datetime import datetime

from llm_client import LocalLLM
from models import DraftInput, DraftOutput, DataPoint
from preference_store import PreferenceStore  # ✅ NEW


class DraftingAgent:
    """
    Drafting agent that turns data points into a REAL business memo email.

    Minimal realism upgrades:
    - Memo MUST NOT include sources / CASE IDs in the email body.
    - Memo uses a realistic layout: Subject / To / From / Date / paragraphs / Key Action Items.
    - No "Key evidence" section in the email body.
    - Uses ONLY provided data points (no invented facts).

    NEW:
    - Auto-adjusts base prompt using learned preferences from SQLite feedback_log.
    """

    def __init__(self, model_name: str = "phi3"):
        self.llm = LocalLLM(model_name=model_name)
        self.pref_store = PreferenceStore()  # ✅ NEW

    def _format_data_points(self, data_points: List[DataPoint]) -> str:
        lines = []
        for dp in data_points:
            lines.append(f"- {dp.text}")
        return "\n".join(lines) if lines else "- [no data points provided]"

    def _length_instruction(self, edit_request: Optional[str]) -> str:
        if not edit_request:
            return "Length: 2 short paragraphs + action items. Keep under ~180 words."

        req = edit_request.lower()

        if "3 lines" in req or "three lines" in req:
            return "Length: EXACTLY 3 sentences total in the body (excluding headers and closing)."
        if "shorter" in req or "concise" in req or "summary" in req:
            return "Length: 3–5 sentences total in the body (excluding headers and closing)."

        return "Length: 2 short paragraphs + action items. Keep under ~180 words."

    # ✅ NEW
    def _preference_instructions(self, edit_request: Optional[str]) -> str:
        prefs = self.pref_store.get_global_preferences()
        instructions = []

        if prefs.get("prefer_more_professional"):
            instructions.append(
                "- Tone preference (learned): Use a more professional/formal tone. Avoid casual phrasing."
            )

        # Apply learned length preference only if user didn’t explicitly force length in edit_request
        req = (edit_request or "").lower()
        user_forced_length = any(
            x in req for x in [
                "3 lines", "three lines", "shorter", "concise", "summary",
                "longer", "more detail", "too short", "too long"
            ]
        )

        if not user_forced_length:
            if prefs.get("prefer_short"):
                instructions.append("- Length preference (learned): Keep it shorter than usual.")
            elif prefs.get("prefer_long"):
                instructions.append("- Length preference (learned): Add slightly more detail than usual.")

        return "\n".join(instructions) if instructions else "- No learned preferences yet."

    def _postprocess(self, email_text: str) -> str:
        text = email_text

        text = re.sub(
            r"(?is)\n\s*Key evidence\s*:\s*\n.*?(?=\n\s*(Key Action Items|Action items|Kind regards|Best regards)\s*:?)",
            "\n",
            text
        )
        text = re.sub(r"\bCASE_[A-Z0-9]+\b", "", text)
        text = re.sub(r"(?i)\bsource\s*:\s*", "", text)

        text = re.sub(r"[ \t]{2,}", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()

        return text

    def run(self, draft_input: DraftInput) -> DraftOutput:
        topic = draft_input.topic
        data_points = draft_input.data_points
        edit_request = draft_input.edit_request
        version = draft_input.version

        data_points_text = self._format_data_points(data_points)
        length_instruction = self._length_instruction(edit_request)

        # ✅ NEW: read learned preferences and inject into prompt
        learned_prefs = self._preference_instructions(edit_request)

        today = datetime.now().strftime("%d %B %Y")

        prompt = f"""
You are an assistant that writes REAL corporate email memos in English.

HARD RULES:
- Use ONLY the DATA POINTS below as factual content. Do NOT invent facts.
- Do NOT include sources, CASE IDs, or the word "source" anywhere in the memo.
- Do NOT include a section called "Key evidence".
- Do NOT claim comparisons (vs Q2, increase/decrease, trends) unless explicitly stated in the data points.
- Keep writing executive-friendly: short paragraphs, clear actions, no meta commentary.

Topic: "{topic}"

DATA POINTS (facts you may use):
{data_points_text}

User edit request (highest priority if present):
{edit_request or "[no specific edit request]"}

Learned preferences from past feedback (apply unless they conflict with the user's edit request):
{learned_prefs}

Length constraint:
- {length_instruction}

WRITE EXACTLY THIS FORMAT:

Subject: <short subject line about {topic}>

To: Sales & Marketing Teams
From: [Your Name], Sales Operations
Date: {today}

Dear Colleagues,

<Paragraph 1: what this memo is + factual summary using the data points.>

<Paragraph 2: brief implications based only on the data points. If anything is unclear, write: "Some figures require validation (TBD).">

Key Action Items:
- 3 short bullets (no numbers, no dates, no meetings)

Please reach out if further clarification is required.

Kind regards,
[Your Name]

Return ONLY the memo text in this exact format.
""".strip()

        email_text = self.llm.run(prompt)
        email_text = self._postprocess(email_text)

        subject = f"Business memo regarding {topic} (v{version})"

        return DraftOutput(
            subject=subject,
            body=email_text,
            version=version,
        )
