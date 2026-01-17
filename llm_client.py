import subprocess


class LocalLLM:
    """
    Uses Ollama to run a FREE local model.
    """

    def __init__(self, model_name="llama3.2:3b"):
        self.model = model_name

    def generate_email(self, prompt: str) -> str:
        result = subprocess.run(
            ["ollama", "run", self.model],
            input=prompt.encode("utf-8"),
            capture_output=True
        )
        return result.stdout.decode("utf-8")

    # NEW: generic interface used by DraftingAgent
    def run(self, prompt: str) -> str:
        """
        Generic 'run' method so other components can call the LLM
        without caring about the underlying implementation.
        """
        return self.generate_email(prompt)
