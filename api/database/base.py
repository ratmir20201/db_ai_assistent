from typing import Tuple

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Создает таблицу - название класса + 's'."""
        result_table_name = ""
        class_name = cls.__name__
        for index in range(len(class_name) - 1):
            result_table_name += class_name[index]
            if class_name[index + 1].isupper():
                result_table_name += "_"
        result_table_name += class_name[-1]

        return result_table_name.lower() + "s"

    repr_cols_num = 3
    repr_cols: Tuple[str, ...] = tuple()

    def __repr__(self):
        """
        Выводит класс и некоторые его колонки.

        Количество колонок можно указать в аргументе repr_cols_num,
        а какие-то определенные колонки можно указать в repr_cols.
        """
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(
                    "{col_name}={col_value}".format(
                        col_name=col,
                        col_value=getattr(self, col),
                    )
                )

        return "<{class_name}({cols})>".format(
            class_name=self.__class__.__name__,
            cols=", ".join(cols),
        )