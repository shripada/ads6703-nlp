"""Every test gets a fresh in-memory database, a fake BERT and a fake LLM. No model file or Groq key needed."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.db import get_session
from app.main import app, classifier, llm


class FakeClassifier:
    def predict(self, text):
        return ("complaint" if "late" in text.lower() else "other"), 0.9


class FakeLlm:
    def __init__(self):
        self.calls = 0

    def complete(self, system, user):
        self.calls += 1
        return f"answer to: {user}"


@pytest.fixture
def fake_llm():
    return FakeLlm()


@pytest.fixture
def client(fake_llm):
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)

    def session_override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = session_override
    app.dependency_overrides[classifier] = FakeClassifier
    app.dependency_overrides[llm] = lambda: fake_llm
    yield TestClient(app)
    app.dependency_overrides.clear()
