from fastapi import Depends
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from database.db import get_async_session


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[int]):
    """Модель токена для аутентификации."""

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )


async def get_access_token_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
