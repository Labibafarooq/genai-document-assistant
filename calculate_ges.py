import csv

def calculate_ges(log_filepath: str) -> dict:
    total = 0
    approved = 0
    grounded_approved = 0
    total_revisions = 0

    with open(log_filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    if not rows:
        return {
            "ges": 0.0,
            "approval_rate": 0.0,
            "avg_revision_cycles": 0.0,
            "groundedness_rate": 0.0
        }

    for row in rows:
        total += 1
        raw = (row.get("revision_cycles") or "").strip()
        try:
            rev_cycles = int(raw)
        except ValueError:
            rev_cycles = 0   

        total_revisions += rev_cycles
        if row.get("final_decision", "").strip().lower() == "approve":
            approved += 1
            if row.get("grounded", "").strip().lower() == "true":
                grounded_approved += 1

    approval_rate = approved / total if total else 0.0
    avg_revision_cycles = total_revisions / total if total else 0.0
    avg_revisions_normalized = min(1.0, avg_revision_cycles / 3.0)
    groundedness_rate = grounded_approved / approved if approved else 0.0

    ges = (
        0.5 * approval_rate +
        0.3 * (1 - avg_revisions_normalized) +
        0.2 * groundedness_rate
    )

    return {
        "ges": ges,
        "approval_rate": approval_rate,
        "avg_revision_cycles": avg_revision_cycles,
        "groundedness_rate": groundedness_rate
    }
