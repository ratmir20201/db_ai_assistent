from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from models.mixins.id_int_pk import IdIntPkMixin


class BotMessage(Base, IdIntPkMixin):
    llm_text: Mapped[str]
    user_question: Mapped[str]
    translated_user_question: Mapped[str | None]

    review: Mapped["MessageReview"] = relationship(
        back_populates="message",
        uselist=False,
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("llm_text", "user_question", name="uq_llm_text_user_question"),
    )
