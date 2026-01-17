# feedback_logger.py

from datetime import datetime
from database import get_connection


class FeedbackLoggerSQL:
    """
    Logs user rating + free-text feedback into feedback_log (SQLite).
    """

    def log_feedback(self, topic: str, revision_cycles: int,
                     rating_1_to_5: int | None, feedback_text: str | None):
        timestamp = datetime.now().isoformat(timespec="seconds")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO feedback_log (timestamp, topic, revision_cycles,
                                      rating_1_to_5, feedback_text)
            VALUES (?, ?, ?, ?, ?)
            """,
            (timestamp, topic, revision_cycles, rating_1_to_5, feedback_text),
        )
        conn.commit()
        conn.close()
