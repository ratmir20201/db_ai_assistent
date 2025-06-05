from typing import Optional

from fastapi import Request, Depends
from fastapi_users import BaseUserManager, IntegerIDMixin

from config import settings
from logger import logger
from models.user import User, get_user_db


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info("User %s has registered.", user.id)

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
    ):
        logger.info(
            "User %s has forgot their password. Reset token: %s",
            user.id,
            token,
        )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
    ):
        logger.info(
            "Verification requested for user %s. Verification token: %s",
            user.id,
            token,
        )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
