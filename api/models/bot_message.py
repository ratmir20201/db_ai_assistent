from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from models.mixins.id_int_pk import IdIntPkMixin


class BotMessage(Base, IdIntPkMixin):
    text: Mapped[str] = mapped_column(unique=True)

    review: Mapped["MessageReview"] = relationship(
        back_populates="message",
        uselist=False,
        cascade="all, delete-orphan",
    )
