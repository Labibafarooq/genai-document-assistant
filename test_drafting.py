from models import DraftInput, DraftOutput
from llm_client import LocalLLM


class DraftingAgent:
    """
    Drafts a clean business memo using a local LLaMA model.
    """

    def __init__(self):
        self.current_version = 0
        self.llm = LocalLLM("llama3.2:3b")

    def run(self, draft_input: DraftInput) -> DraftOutput:
        self.current_version += 1

        points_text = "\n".join(f"- {dp.text}" for dp in draft_input.data_points)

        prompt = f"""
Write a professional business memo email.

Topic: {draft_input.topic}

Key data points:
{points_text}

{f"The user requested these changes: {draft_input.edit_request}" if draft_input.edit_request else ""}

Your output:
- Start with "Dear team,"
- Write a clear, concise business memo
- End with a polite closing
- Do NOT include a subject line
        """

        body = self.llm.generate_email(prompt)

        subject = f"Business memo regarding {draft_input.topic} (v{self.current_version})"

        return DraftOutput(subject=subject, body=body, version=self.current_version)
