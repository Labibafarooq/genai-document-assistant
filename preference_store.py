# preference_store.py

from collections import Counter
from typing import Dict, Any

from database import get_connection


class PreferenceStore:
    """
    Reads feedback_log table in SQLite and extracts SIMPLE global preferences like:
      - prefer_short
      - prefer_long
      - prefer_more_professional
    """

    def _load_rows(self) -> list[dict]:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT rating_1_to_5, feedback_text
            FROM feedback_log
            """
        )
        rows = []
        for row in cur.fetchall():
            rows.append({
                "rating_1_to_5": row["rating_1_to_5"],
                "feedback_text": row["feedback_text"] or "",
            })
        conn.close()
        return rows

    def get_global_preferences(self) -> Dict[str, Any]:
        rows = self._load_rows()
        if not rows:
            return {
                "prefer_short": False,
                "prefer_long": False,
                "prefer_more_professional": False,
            }

        counts = Counter()

        for row in rows:
            text = (row["feedback_text"] or "").lower()

            if not text.strip():
                continue

            # Length hints
            if any(p in text for p in ["too long", "very long", "shorter"]):
                counts["too_long"] += 1
            if any(p in text for p in ["too short", "longer", "more detail"]):
                counts["too_short"] += 1

            # Tone hints
            if any(p in text for p in ["more professional", "professional tone", "more formal"]):
                counts["more_professional"] += 1

        prefer_short = counts["too_long"] > counts["too_short"]
        prefer_long = counts["too_short"] > counts["too_long"]
        prefer_more_professional = counts["more_professional"] > 0

        return {
            "prefer_short": prefer_short,
            "prefer_long": prefer_long,
            "prefer_more_professional": prefer_more_professional,
        }
