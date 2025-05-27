from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from models.mixins.id_int_pk import IdIntPkMixin


class MessageReview(Base, IdIntPkMixin):
    likes: Mapped[int]
    dislikes: Mapped[int]

    message_id: Mapped[int] = mapped_column(
        ForeignKey("bot_messages.id", ondelete="CASCADE")
    )
