from sqlalchemy.orm import Session

from models.bot_message import BotMessage
from models.message_review import MessageReview


def create_bot_message(session: Session, response_text: str) -> int:
    message = BotMessage(text=response_text)
    review = MessageReview(likes=0, dislikes=0)
    message.review = review

    session.add(message)
    session.commit()

    return message.id
