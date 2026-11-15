"""Database tables. Replace Text with the things your app stores (tickets, reviews, transactions…)."""
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def now() -> datetime:
    return datetime.now(timezone.utc)


class Text(SQLModel, table=True):
    """A text the user sent, and the label BERT gave it."""
    id: int | None = Field(default=None, primary_key=True)
    body: str
    label: str
    score: float
    created_at: datetime = Field(default_factory=now)


class LlmAnswer(SQLModel, table=True):
    """Saved LLM answers, so the same prompt is never sent to Groq twice."""
    prompt_hash: str = Field(primary_key=True)
    answer: str
    created_at: datetime = Field(default_factory=now)
