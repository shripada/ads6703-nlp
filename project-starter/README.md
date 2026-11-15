# Starter app: React + FastAPI + Postgres + BERT (ONNX) + Groq, on Vercel

This is the starting point for your ADS 6703 mini project. It already works end to end:
you type a text, your BERT model labels it, the result is saved in the database, and an LLM endpoint
answers questions through Groq. Your job is to turn it into your app.

```
├── frontend/          React (Vite). Screens in src/, every back-end call in src/api.js
├── backend/app/       FastAPI. main.py (routes), models.py (tables), bert.py, llm.py, db.py
├── backend/tests/     pytest tests. They use a fake BERT and a fake LLM
├── api/index.py       Vercel's entry point. It just loads backend/app
├── model/             your exported BERT: model.onnx, tokenizer.json, config.json
├── docs/              grilling.md, prd.md, review.md, export-bert.md
├── CLAUDE.md          the rules your coding agent follows
├── requirements.txt   what Vercel installs (keep it small)
└── vercel.json        build settings and the /api route
```

## 1. Make it your team's repo

Copy this folder out of your course folder, then:

```
cd <your-project-folder>
git init && git add . && git commit -m "Start from the course starter"
```

Create an empty repo on GitHub, push to it, and add your teammates and the instructor.

## 2. Run it on your laptop

You need [uv](https://docs.astral.sh/uv/) and [Node.js](https://nodejs.org/) 20 or later.

```
cp .env.example .env                  # then paste your Groq key into .env
uv venv --python 3.12
uv pip install -r backend/requirements-dev.txt

cd backend
uv run pytest                         # all tests should pass
uv run --env-file ../.env uvicorn app.main:app --reload --port 8000
```

In a second terminal:

```
cd frontend
npm install
npm run dev                           # open the link it prints
```

Until you put a model in `model/`, labelling a text says "No model.onnx". The LLM part works as soon
as your key is in `.env`.

## 3. Add your BERT model

Fine-tune in Colab, then export and shrink it as described in [docs/export-bert.md](docs/export-bert.md).
Put the three files in `model/`. If `model.onnx` is over 100 MB, put it on the Hugging Face Hub instead
and ask your agent to download it at start-up.

## 4. Deploy on Vercel

1. On [vercel.com](https://vercel.com), sign in with GitHub and import your repo. Keep the default settings: `vercel.json` sets them.
2. In the project, open **Storage** → **Create** → **Neon** (Postgres). It adds `DATABASE_URL` for you.
3. In **Settings → Environment Variables**, add `GROQ_API_KEY` and `GROQ_MODEL`.
4. Redeploy. Open `https://<your-app>.vercel.app/api/health`: it should say `{"ok": true}`.

Every push to `main` deploys again. Deploy early, on day 3, not on the last night.

## 5. Install the skills

In Claude Code:

```
/plugin marketplace add mattpocock/skills
/plugin install mattpocock-skills@mattpocock
```

For other agents: `npx skills add mattpocock/skills`. Then start with the grilling skill, as the
project page explains.
