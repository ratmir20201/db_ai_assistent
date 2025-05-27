from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from database.db import get_session
from models.message_review import MessageReview

router = APIRouter(tags=["Review"])


@router.post("/messages/{message_id}/like")
def add_like(message_id: int, session: Session = Depends(get_session)):
    review = session.get(MessageReview, message_id)
    if not review:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Сообщение не найдено.",
        )

    review.likes += 1
    session.commit()

    return {"message": "success"}


@router.post("/messages/{message_id}/dislike")
def add_dislike(message_id: int, session: Session = Depends(get_session)):
    review = session.get(MessageReview, message_id)
    if not review:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Сообщение не найдено.",
        )

    review.dislikes += 1
    session.commit()

    return {"message": "success"}
