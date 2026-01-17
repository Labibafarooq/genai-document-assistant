import csv
from pathlib import Path
from statistics import mean
from collections import Counter


def load_evaluation_log(filepath: str = "evaluation_log.csv"):
    path = Path(filepath)
    if not path.exists():
        print(f"No evaluation_log.csv found at {path.resolve()}")
        return []

    rows = []
    with path.open(mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert revision_cycles to int safely
            try:
                row["revision_cycles"] = int(row["revision_cycles"])
            except (ValueError, KeyError):
                row["revision_cycles"] = 0
            rows.append(row)
    return rows


def main():
    rows = load_evaluation_log()
    if not rows:
        print("No data to analyze yet. Run business_memo_system.py a few times first.")
        return

    total_runs = len(rows)
    decisions = [r["final_decision"] for r in rows]
    revision_cycles = [r["revision_cycles"] for r in rows]

    decision_counts = Counter(decisions)
    approved = decision_counts.get("approve", 0)
    rejected = decision_counts.get("reject", 0)

    avg_revision_cycles = mean(revision_cycles)

    print("=== Business Memo System – Evaluation Summary ===")
    print(f"Total runs: {total_runs}")
    print(f"Approved: {approved}")
    print(f"Rejected: {rejected}")
    print(f"Approval rate: {approved / total_runs * 100:.1f}%")
    print(f"Average revision cycles: {avg_revision_cycles:.2f}")

    # Optional: per-topic stats
    print("\nPer-topic average revision cycles:")
    topic_to_cycles = {}
    for r in rows:
        topic = r["topic"]
        topic_to_cycles.setdefault(topic, []).append(r["revision_cycles"])

    for topic, cycles in topic_to_cycles.items():
        print(f"  - {topic!r}: {mean(cycles):.2f} (runs: {len(cycles)})")


if __name__ == "__main__":
    main()
