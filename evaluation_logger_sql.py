# evaluation_logger_sql.py

from datetime import datetime
from database import get_connection


class EvaluationLoggerSQL:
    """
    Logs each run into the SQLite table evaluation_log.
    """

    def log(self, topic: str, revision_cycles: int, final_decision: str):
        timestamp = datetime.now().isoformat(timespec="seconds")

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO evaluation_log (timestamp, topic, revision_cycles, final_decision)
            VALUES (?, ?, ?, ?)
            """,
            (timestamp, topic, revision_cycles, final_decision),
        )
        conn.commit()
        conn.close()
