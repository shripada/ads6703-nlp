"""Calls the Groq LLM. The key is read from the environment on the server and never reaches the browser."""
import os


class LlmNotConfigured(RuntimeError):
    pass


class GroqLlm:
    def __init__(self):
        key = os.environ.get("GROQ_API_KEY")
        if not key:
            raise LlmNotConfigured("GROQ_API_KEY is not set. Put it in .env locally, or in Vercel's settings.")
        from groq import Groq

        self.client = Groq(api_key=key)
        self.model = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")

    def complete(self, system: str, user: str) -> str:
        reply = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.2,
            max_tokens=500,
        )
        return reply.choices[0].message.content or ""


def get_llm() -> GroqLlm:
    """A new client per request. Tests replace the llm() dependency in main.py, so they never call Groq."""
    return GroqLlm()
