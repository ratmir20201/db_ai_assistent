from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from models.mixins.id_int_pk import IdIntPkMixin


class BotMessage(Base, IdIntPkMixin):
    text: Mapped[str]
