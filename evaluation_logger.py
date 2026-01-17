import csv
import os
from datetime import datetime


class EvaluationLogger:
    def __init__(self, filepath: str = "evaluation_log.csv"):
        self.filepath = filepath

    def log(self, topic: str, revision_cycles: int, final_decision: str, grounded: bool):
        file_exists = os.path.exists(self.filepath)

        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp", "topic", "grounded", "revision_cycles", "final_decision"])
            writer.writerow([datetime.utcnow().isoformat(), topic, grounded, revision_cycles, final_decision])
