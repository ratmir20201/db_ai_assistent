from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from auth.auth_routers import fastapi_users
from crud.message_feedback import add_like_to_message, add_dislike_to_message
from database.db import get_session
from models.user import User

router = APIRouter(tags=["Review"])


@router.post("/messages/{message_id}/like")
def add_like(
    message_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(fastapi_users.current_user()),
) -> dict:
    add_like_to_message(message_id=message_id, session=session, user=user)

    return {"message": "success"}


@router.post("/messages/{message_id}/dislike")
def add_dislike(
    message_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(fastapi_users.current_user()),
) -> dict:
    add_dislike_to_message(message_id=message_id, session=session, user=user)

    return {"message": "success"}
