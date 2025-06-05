import datetime

from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from models.mixins.id_int_pk import IdIntPkMixin


# TODO: Удалить таблицу message_reviews и убрать None в полях model_used, user_id
class BotMessage(Base, IdIntPkMixin):
    llm_text: Mapped[str]
    user_question: Mapped[str]
    translated_user_question: Mapped[str | None]
    model_used: Mapped[str | None]
    timestamp: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('UTC', now())")
    )
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )

    feedbacks: Mapped[list["MessageFeedback"]] = relationship(
        back_populates="message",
        cascade="all, delete-orphan",
    )

    # review: Mapped["MessageReview"] = relationship(
    #     back_populates="message",
    #     uselist=False,
    #     cascade="all, delete-orphan",
    # )
