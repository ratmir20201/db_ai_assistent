from fastapi import Request, HTTPException
from fastapi_users.password import PasswordHelper
from sqladmin import ModelView
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from wtforms import PasswordField

from admin.user_creation import add_user_to_db
from database.db import get_async_context_session
from models.access_token import AccessToken
from models.user import User
from schemas import UserCreate

password_helper = PasswordHelper()


async def get_user_by_token(token: str, session: AsyncSession) -> User | None:
    """Отдает пользователя по его токену."""
    result = await session.execute(
        select(AccessToken).where(AccessToken.token == token)
    )
    access_token = result.scalar_one_or_none()

    if not access_token:
        return None

    result = await session.execute(select(User).where(User.id == access_token.user_id))
    return result.scalar_one_or_none()


class AdminModelView(ModelView):
    async def is_accessible(self, request: Request) -> bool:
        token = request.cookies.get("accessToken")
        if not token:
            raise HTTPException(status_code=401, detail="Неавторизован")

        async with get_async_context_session() as session:
            user = await get_user_by_token(token, session)
            if not user or not user.is_superuser:
                raise HTTPException(
                    status_code=403,
                    detail="У вас нет прав доступа к админ-панели",
                )

        return True


class UserAdmin(AdminModelView, model=User):
    form_extra_fields = {
        "password": PasswordField("Password"),
    }
    # form_columns = ["email", "username", "password", "is_superuser"]

    async def on_model_change(self, form, model, is_created):
        user_create = UserCreate(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )
        user = await add_user_to_db(user_create)
        model.id = user.id
        model.hashed_password = user.hashed_password

        return await super().on_model_change(form, model, is_created)
