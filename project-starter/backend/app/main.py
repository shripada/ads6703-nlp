"""The FastAPI app. Every route starts with /api, because Vercel sends /api/... here (see vercel.json).

The routes below are a small working example: send a text, BERT labels it and it is saved, and an
LLM endpoint that saves its answers. Replace them with your own app, one GitHub issue at a time, tests first.
"""
import hashlib
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from .bert import ModelMissing, get_classifier
from .db import create_tables, get_session
from .llm import LlmNotConfigured, get_llm
from .models import LlmAnswer, Text


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="Starter app", lifespan=lifespan)


class TextIn(BaseModel):
    body: str = Field(min_length=1, max_length=5000)


class AskIn(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


def classifier():
    try:
        return get_classifier()
    except ModelMissing as e:
        raise HTTPException(503, str(e))


def llm():
    try:
        return get_llm()
    except LlmNotConfigured as e:
        raise HTTPException(503, str(e))


@app.get("/api/health")
def health():
    return {"ok": True}


@app.post("/api/texts", response_model=Text, status_code=201)
def add_text(data: TextIn, session: Session = Depends(get_session), model=Depends(classifier)):
    label, score = model.predict(data.body)
    text = Text(body=data.body, label=label, score=score)
    session.add(text)
    session.commit()
    session.refresh(text)
    return text


@app.get("/api/texts", response_model=list[Text])
def list_texts(session: Session = Depends(get_session)):
    return session.exec(select(Text).order_by(Text.created_at.desc()).limit(50)).all()


SYSTEM_PROMPT = "You are a helpful assistant inside a small business app. Answer in at most five sentences."


@app.post("/api/ask")
def ask(data: AskIn, session: Session = Depends(get_session), model=Depends(llm)):
    key = hashlib.sha256((SYSTEM_PROMPT + "\n" + data.question).encode()).hexdigest()
    if saved := session.get(LlmAnswer, key):
        return {"answer": saved.answer, "saved": True}
    answer = model.complete(SYSTEM_PROMPT, data.question)
    session.add(LlmAnswer(prompt_hash=key, answer=answer))
    session.commit()
    return {"answer": answer, "saved": False}
