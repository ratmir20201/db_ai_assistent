import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from models.mixins.id_int_pk import IdIntPkMixin


class MessageReview(Base, IdIntPkMixin):
    likes: Mapped[int]
    dislikes: Mapped[int]

    message_id: Mapped[int] = mapped_column(
        ForeignKey("bot_messages.id", ondelete="CASCADE"),
        unique=True,
    )
    # message: Mapped["BotMessage"] = relationship(back_populates="review")


class MessageFeedback(Base, IdIntPkMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    message_id: Mapped[int] = mapped_column(
        ForeignKey("bot_messages.id", ondelete="CASCADE")
    )
    like_status: Mapped[str]
    timestamp: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('UTC', now())")
    )

    message: Mapped["BotMessage"] = relationship(back_populates="feedbacks")

    __table_args__ = (UniqueConstraint("user_id", "message_id"),)
