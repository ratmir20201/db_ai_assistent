from sqlalchemy import select
from sqlalchemy.orm import Session

from models.bot_message import BotMessage
from models.message_review import MessageReview


def create_bot_message(
    session: Session,
    llm_text: str,
    user_question: str,
    translated_user_question: str | None = None,
) -> int:
    existing_id = get_existing_message_id(session, llm_text, user_question)
    if existing_id is not None:
        return existing_id

    message = BotMessage(
        llm_text=llm_text,
        user_question=user_question,
        translated_user_question=translated_user_question,
    )
    review = MessageReview(likes=0, dislikes=0)
    message.review = review

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
