from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from database.db import get_async_session
from models.mixins.id_int_pk import IdIntPkMixin


class User(Base, IdIntPkMixin, SQLAlchemyBaseUserTable[int]):
    """Модель пользователя."""

    username: Mapped[str] = mapped_column(unique=True)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
