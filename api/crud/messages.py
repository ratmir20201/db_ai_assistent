from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from models.bot_message import BotMessage


def create_bot_message(
    session: Session,
    llm_text: str,
    user_question: str,
    llm_model: str,
    user_id: int,
    translated_user_question: str | None = None,
) -> int:
    existing_id = get_existing_message_id(session, llm_text, user_question)
    if existing_id is not None:
        return existing_id

    message = BotMessage(
        llm_text=llm_text,
        user_question=user_question,
        translated_user_question=translated_user_question,
        model_used=llm_model,
        user_id=user_id,
    )

    session.add(message)
    session.commit()

    return message.id


def get_existing_message_id(
    session: Session,
    llm_text: str,
    user_question: str,
) -> int | None:
    existing = session.scalar(
        select(BotMessage).where(
            BotMessage.llm_text == llm_text,
            BotMessage.user_question == user_question,
        )
    )

    if existing:
        return existing.id

    return None


def get_message_by_id(
    message_id: int,
    session: Session,
) -> BotMessage:
    message = session.get(BotMessage, message_id)
    if not message:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Сообщение не найдено.",
        )

    return message
