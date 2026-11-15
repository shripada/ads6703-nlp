# Project rules for the coding agent

This is a student team's ADS 6703 (NLP) mini project. The team must understand and explain every
part of it, so explain your changes in plain words as you go, and keep the code simple.

## Stack (do not change)

- Front end: React with Vite, in `frontend/`. Plain CSS. Every back-end call goes through `frontend/src/api.js`.
- Back end: FastAPI in `backend/app/`, served on Vercel through `api/index.py`. Every route starts with `/api`.
- Database: SQLModel. SQLite locally, Neon Postgres on Vercel (`DATABASE_URL`). Tables in `backend/app/models.py`.
- BERT: a fine-tuned model exported to ONNX in `model/`, run with `onnxruntime` and `tokenizers` (`backend/app/bert.py`).
- LLM: Groq, through `backend/app/llm.py`. Model name from `GROQ_MODEL`.

## Hard rules

- Never add `torch`, `transformers` or other large packages to `requirements.txt`. The Vercel bundle must stay under 500 MB. Training happens in a notebook, not in the app.
- The Groq key is read only in the back end, from the environment. Never put it in front-end code, in a committed file, or in a log.
- Save LLM answers in the database (see `LlmAnswer`), so a repeated prompt does not use the free quota again.
- Never send real personal data to the LLM. The demo uses public or made-up texts.
- Tests never call Groq or need a model file: they replace the `classifier` and `llm` dependencies with fakes (see `backend/tests/conftest.py`).

## How we work

- Words: use the terms in `CONTEXT.md`. If a new idea needs a name, add it there first.
- Plan: work from the GitHub issues made from `docs/prd.md`, one issue at a time.
- Back end: test-first. Write a failing test in `backend/tests/`, run it and see it fail, write the code, run `uv run pytest` and see it pass, then tidy up. Commit the test and the code so the history shows the test came first.
- Before the final merge, run the code-review skill and save its findings in `docs/review.md`.

## Commands

- Back-end tests: `cd backend && uv run pytest`
- Back end: `cd backend && uv run --env-file ../.env uvicorn app.main:app --reload --port 8000`
- Front end: `cd frontend && npm run dev`
