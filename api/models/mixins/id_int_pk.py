from sqlalchemy.orm import Mapped, mapped_column


class IdIntPkMixin:
    """Миксин создания id для таблицы."""

    id: Mapped[int] = mapped_column(primary_key=True)