"""The database connection. Locally: a SQLite file. On Vercel: Neon Postgres, from DATABASE_URL."""
import os

from sqlmodel import Session, SQLModel, create_engine


def database_url() -> str:
    url = os.environ.get("DATABASE_URL", "")
    if not url:
        return "sqlite:///./local.db"
    # Neon gives postgres://...; SQLAlchemy needs to be told to use the psycopg 3 driver.
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix):]
    return url


engine = create_engine(database_url(), pool_pre_ping=True)


def create_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
