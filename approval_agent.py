from models import DraftOutput, ApprovalOutput


class ApprovalAgent:
    """
    Human-in-the-loop agent.
    Shows the draft to the user and collects:
    - approve
    - edit_request
    """

    def run(self, draft: DraftOutput) -> ApprovalOutput:
        print("\n===== EMAIL DRAFT =====")
        print(f"{draft.subject}\n")
        print(draft.body)
        print("\n=======================\n")

        while True:
            choice = input("Type 'a' = approve, 'e' = edit_request: ").strip().lower()

            if choice == "a":
                return ApprovalOutput(decision="approve")

            if choice == "e":
                edit_text = input("Describe the edits you want: ").strip()
                if not edit_text:
                    edit_text = "Please improve clarity and conciseness."
                return ApprovalOutput(decision="edit_request", edit_request=edit_text)

            print("Invalid input. Please type 'a' or 'e'.")
