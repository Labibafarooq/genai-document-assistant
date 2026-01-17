"""Utility script to print the latest Global Evaluation Score (GES).

Run this after collecting new evaluation_log.csv entries to get a quick
snapshot of approval rate, revision efficiency, and groundedness.
"""

from calculate_ges import calculate_ges

if __name__ == "__main__":
    result = calculate_ges("evaluation_log.csv")
    print("Global Evaluation Score (GES) Results:")
    for k, v in result.items():
        print(f"{k}: {v}")
