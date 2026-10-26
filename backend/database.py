"""SQLAlchemy engine and session helpers."""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from config import settings

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    # Import models so metadata is registered before create_all.
    import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _ensure_sqlite_user_role_column()


def _ensure_sqlite_user_role_column() -> None:
    """create_all will not add columns to an existing users table."""
    if not settings.database_url.startswith("sqlite"):
        return
    with engine.connect() as conn:
        rows = conn.execute(text("PRAGMA table_info(users)")).fetchall()
        names = {row[1] for row in rows}
        if "role" in names:
            return
        conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(16) DEFAULT 'seeker'"))
        conn.commit()
