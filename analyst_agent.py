import csv
import os
import re
from typing import List, Optional, Set

from models import AnalystOutput, DataPoint


class AnalystAgent:
    """
    Simple dataset retriever (no extra dependencies).
    Loads a CSV of cases and retrieves the most relevant gold_data_points.

    NEW:
    - Supports exclude_sources: when provided, it will skip rows whose case_id is already used.
    """

    def __init__(self, csv_path: str = "business_memo_cases_20k.csv", top_k: int = 3):
        self.csv_path = csv_path
        self.top_k = top_k
        self.rows = self._load_rows()

    def _load_rows(self) -> List[dict]:
        if not os.path.exists(self.csv_path):
            alt = "business_memo_cases.csv"
            if os.path.exists(alt):
                self.csv_path = alt
            else:
                return []

        rows = []
        with open(self.csv_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append(r)
        return rows

    def _tokenize(self, text: str) -> set:
        return set(re.findall(r"[a-z0-9]+", (text or "").lower()))

    def run(self, topic: str, exclude_sources: Optional[Set[str]] = None) -> AnalystOutput:
        """
        Retrieve relevant data points for the topic.
        If exclude_sources is provided, rows with case_id in exclude_sources are skipped.
        """
        if not self.rows:
            return AnalystOutput(topic=topic, data_points=[])

        exclude_sources = exclude_sources or set()

        q = self._tokenize(topic)
        scored = []

        for r in self.rows:
            case_id = (r.get("case_id") or "UNKNOWN_CASE").strip()

            # ✅ NEW: skip already-used cases
            if case_id in exclude_sources:
                continue

            corpus = " ".join([
                r.get("topic", "") or "",
                r.get("audience", "") or "",
                r.get("tone", "") or "",
                r.get("evidence_pack", "") or "",
                r.get("gold_data_points", "") or "",
            ])

            tokens = self._tokenize(corpus)
            score = len(q & tokens)
            scored.append((score, r))

        scored.sort(key=lambda x: x[0], reverse=True)

        # threshold to avoid random matches
        best = [r for s, r in scored[: self.top_k] if s >= 2]
        if not best:
            return AnalystOutput(topic=topic, data_points=[])

        data_points: List[DataPoint] = []
        for r in best:
            case_id = (r.get("case_id") or "UNKNOWN_CASE").strip()
            gold = r.get("gold_data_points", "") or ""

            for dp in [x.strip() for x in gold.split("|") if x.strip()]:
                data_points.append(DataPoint(text=dp, source=case_id))

        # limit to avoid noisy drafts
        return AnalystOutput(topic=topic, data_points=data_points[:8])
