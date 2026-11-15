"""Vercel's entry point. Every /api/... request comes here (see vercel.json). The app itself is in backend/app/."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.main import app  # noqa: E402,F401
