from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from crud.messages import get_message_by_id
from models.message_feedback import MessageFeedback
from models.user import User


def add_like_to_message(
    message_id: int,
    session: Session,
    user: User,
) -> None:
    message = get_message_by_id(message_id=message_id, session=session)
    add_feedback(
        message_id=message.id,
        session=session,
        user_id=user.id,
        like_status="like",
    )


def add_dislike_to_message(
    message_id: int,
    session: Session,
    user: User,
) -> None:
    message = get_message_by_id(message_id=message_id, session=session)
    add_feedback(
        message_id=message.id,
        session=session,
        user_id=user.id,
        like_status="dislike",
    )


def add_feedback(
    message_id: int,
    session: Session,
    user_id: int,
    like_status: str,
) -> None:
    feedback = session.execute(
        select(MessageFeedback).where(
            MessageFeedback.message_id == message_id,
            MessageFeedback.user_id == user_id,
        )
    ).scalar_one_or_none()

    if feedback:
        feedback.like_status = like_status
    else:
        feedback = MessageFeedback(
            user_id=user_id,
            message_id=message_id,
            like_status=like_status,
        )
        session.add(feedback)

    session.commit()
