from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session, sessionmaker

from config import settings

DATABASE_URL = settings.db.db_url
engine = create_engine(DATABASE_URL, echo=settings.db.echo)


_Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)


Base = declarative_base()


def get_session() -> Generator[Session, Any, None]:
    """Функция для получения сессии."""
    db = _Session()
    try:
        yield db
    finally:
        db.close()
