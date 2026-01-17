import csv
import os
from datetime import datetime, timezone
import re
from database import init_db
init_db()

from analyst_agent import AnalystAgent
from drafting_agent import DraftingAgent
from approval_agent import ApprovalAgent
from evaluation_logger import EvaluationLogger
from models import DraftInput, DataPoint


FEEDBACK_FILE = "feedback_memory.csv"


def store_feedback(topic: str, edit_request: str):
    """Store human edit requests as feedback memory (STYLE guidance)."""
    if not edit_request:
        return

    file_exists = os.path.exists(FEEDBACK_FILE)
    with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["topic", "feedback_text", "created_at"])
        writer.writerow([topic, edit_request, datetime.now(timezone.utc).isoformat()])


def is_missing_info_request(edit_request: str | None) -> bool:
    if not edit_request:
        return False
    t = edit_request.lower().strip()

    patterns = [
        r"\bmissing\b",
        r"\badd(itional)?\b",
        r"\bmore info\b",
        r"\bmore details\b",
        r"\bmore information\b",          # ✅ NEW
        r"\bneed more\b",                  # ✅ NEW
        r"\bi need more\b",                # ✅ NEW
        r"\bincomplete\b",
        r"\bnot enough\b",
        r"\bexpand\b",
        r"\binclude all\b",
        r"\bdata\b",
        r"\bnumbers\b",
        r"\bkpi(s)?\b",
        r"\bmetrics\b",
        r"\bprovide\b.*\bdetails\b",       # ✅ NEW (flexible)
        r"\badditional\b.*\binformation\b" # ✅ NEW (flexible)
    ]
    return any(re.search(p, t) for p in patterns)



def merge_datapoints(
    old_points: list[DataPoint],
    new_points: list[DataPoint],
    limit: int = 12
) -> list[DataPoint]:
    """Merge and deduplicate datapoints by (text, source)."""
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
    """Collect current case_ids already used in evidence."""
    return {dp.source for dp in points if dp.source}


class BusinessMemoSystem:
    def __init__(self):
        self.analyst = AnalystAgent()
        self.drafter = DraftingAgent()
        self.approval = ApprovalAgent()
        self.logger = EvaluationLogger()

    def run(self, topic: str, max_revision_cycles: int = 10) -> int:
        print("\n[AnalystAgent] Starting analysis + retrieval...")
        analyst_output = self.analyst.run(topic)
        grounded = len(analyst_output.data_points) > 0
        print(f"[AnalystAgent] Done. Retrieved {len(analyst_output.data_points)} data point(s).")

        if grounded:
            print("[SYSTEM] Grounding: Using dataset evidence (retrieved data points).")
        else:
            print("[SYSTEM] Grounding: No matching dataset evidence found. Draft may rely on general LLM knowledge (TBD placeholders).")

        revision_cycles = 0
        edit_request: str | None = None
        final_decision = "unknown"

        working_points = analyst_output.data_points

        # Debug: show sources used initially
        initial_sources = sorted(get_used_sources(working_points))
        if initial_sources:
            print(f"[DEBUG] Initial evidence sources: {initial_sources}")
        else:
            print("[DEBUG] Initial evidence sources: []")

        while True:
            if revision_cycles >= max_revision_cycles:
                final_decision = "max_cycles_reached"
                print(f"\n⚠️ Max revision cycles reached ({max_revision_cycles}). Stopping.")
                break

            draft_input = DraftInput(
                topic=topic,
                data_points=working_points,
                edit_request=edit_request,
                version=revision_cycles + 1,
                grounded=(len(working_points) > 0),
            )

            print(f"\n[DraftingAgent] Starting drafting (v{draft_input.version})...")
            draft_output = self.drafter.run(draft_input)
            print("[DraftingAgent] Done. Draft ready.")

            print("[ApprovalAgent] Waiting for human decision (approve / edit_request)...")
            approval_output = self.approval.run(draft_output)
            print(f"[ApprovalAgent] Done. Decision = {approval_output.decision}")

            if approval_output.decision == "approve":
                final_decision = "approve"
                print("\n✅ Memo approved!")
                break

            if approval_output.decision == "edit_request":
                revision_cycles += 1
                edit_request = (approval_output.edit_request or "").strip()
                if not edit_request:
                    edit_request = "Please improve clarity and conciseness."

                # If edit request asks for missing/additional info -> rerun AnalystAgent
                if is_missing_info_request(edit_request):
                    print("\n[AnalystAgent] Missing-info request detected. Re-running retrieval...")

                    used_sources = get_used_sources(working_points)
                    print(f"[DEBUG] Excluding already-used sources: {sorted(used_sources)}")

                    # Ask for NEW evidence by excluding already used case IDs
                    query = f"{topic}. User request: {edit_request}"
                    analyst_output_2 = self.analyst.run(query, exclude_sources=used_sources)

                    print(f"[AnalystAgent] Done. Retrieved {len(analyst_output_2.data_points)} additional data point(s).")

                    before = len(working_points)
                    working_points = merge_datapoints(working_points, analyst_output_2.data_points, limit=16)
                    after = len(working_points)

                    print(f"[DEBUG] Evidence size: {before} -> {after}")
                    print(f"[DEBUG] Current evidence sources: {sorted(get_used_sources(working_points))}")

                    if len(working_points) > 0:
                        print("[SYSTEM] Grounding: Updated evidence set will be used in the next draft.")
                    else:
                        print("[SYSTEM] Grounding: Still no dataset evidence found; next draft may include TBD placeholders.")

                    # Do NOT store missing-info requests as feedback: they are content requests
                else:
                    # Style edits are good feedback to reuse later
                    store_feedback(topic, edit_request)

                print(f"\n✏️ Edit requested. Starting revision cycle #{revision_cycles}...")
                continue

            final_decision = "unknown"
            print("\n⚠️ Unknown decision, stopping.")
            break

        self.logger.log(
            topic=topic,
            revision_cycles=revision_cycles,
            final_decision=final_decision,
            grounded=(len(working_points) > 0),
        )

        # --- GES Calculation and Display ---
        # GES = 0.5 * approval_rate + 0.3 * (1 - avg_revisions_normalized) + 0.2 * groundedness_rate
        # where avg_revisions_normalized = min(1.0, avg_revision_cycles / 3.0)
        # - approval_rate: proportion of runs ending in "approve"
        # - avg_revision_cycles: average number of revision cycles (penalized if >3)
        # - groundedness_rate: proportion of approved memos that are grounded
        try:
            from calculate_ges import calculate_ges
            ges_result = calculate_ges("evaluation_log.csv")
            print("\n[Evaluation] Global Evaluation Score (GES) updated:")
            for k, v in ges_result.items():
                print(f"  {k}: {v}")
        except Exception as e:
            print(f"[Evaluation] Could not calculate GES: {e}")

        return revision_cycles


if __name__ == "__main__":
    system = BusinessMemoSystem()
    topic = input("Enter the memo topic: ")
    cycles = system.run(topic, max_revision_cycles=10)
    print(f"\nRun finished. Revision cycles: {cycles}")
