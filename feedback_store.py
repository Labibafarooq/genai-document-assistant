# feedback_store.py

from feedback_logger import FeedbackLoggerSQL


class FeedbackStore:
    """
    High-level helper:
    - asks the user for rating + free-text feedback
    - sends it to FeedbackLoggerSQL to store in DB
    """

    def __init__(self):
        self.logger = FeedbackLoggerSQL()

    def collect_and_save(self, topic: str, revision_cycles: int):
        print("\n📊 FEEDBACK (optional)")
        print("Please rate this memo from 1 (very bad) to 5 (excellent).")

        rating: int | None = None
        rating_str = input("Rating [1–5, or Enter to skip]: ").strip()

        if rating_str:
            try:
                rating_int = int(rating_str)
                if 1 <= rating_int <= 5:
                    rating = rating_int
                else:
                    print("Invalid rating (must be 1–5). Skipping numeric rating.")
            except ValueError:
                print("Could not parse rating. Skipping numeric rating.")

        feedback_text = input(
            "Optional: any feedback about tone / length / content? (Enter to skip): "
        ).strip()

        # If user gave nothing, don't store an empty row
        if rating is None and not feedback_text:
            print("No feedback given.")
            return

        # Store in SQLite via FeedbackLoggerSQL
        self.logger.log_feedback(
            topic=topic,
            revision_cycles=revision_cycles,
            rating_1_to_5=rating,
            feedback_text=feedback_text or None,
        )

        print("✅ Feedback stored in feedback_log table.")
