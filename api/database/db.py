from contextlib import asynccontextmanager
from typing import Any, Generator, AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, Session, sessionmaker

from config import settings

DATABASE_URL = settings.db.db_url
ASYNC_DATABASE_URL = settings.db.async_db_url
engine = create_engine(DATABASE_URL, echo=settings.db.echo)
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=settings.db.echo)


_Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

_AsyncSession = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


def get_session() -> Generator[Session, Any, None]:
    """Функция для получения сессии."""
    db = _Session()
    try:
        yield db
    finally:
        db.close()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Функция для получения асинхронной сессии."""
    async with _AsyncSession() as async_session:
        yield async_session
        await async_session.close()


@asynccontextmanager
async def get_async_context_session() -> AsyncGenerator[AsyncSession, None]:
    """Функция для получения асинхронной сессии используя ее в контекстном менеджере."""
    async with _AsyncSession() as async_session:
        try:
            yield async_session
        finally:
            await async_session.close()
