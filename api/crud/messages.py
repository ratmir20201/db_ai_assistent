from sqlalchemy.orm import Session

from models.bot_message import BotMessage
from models.message_review import MessageReview


def create_bot_message(
    session: Session,
    llm_text: str,
    user_question: str,
    translated_user_question: str | None = None,
) -> int:

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
