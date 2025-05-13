from fastapi import HTTPException
from logger import logger
from schemas import DBType
from sql_executors.sqlite_runner import execute_sqlite_query
from sql_executors.vertica_runner import execute_vertica_query
from starlette.status import HTTP_400_BAD_REQUEST

WRITE_COMMANDS = (
    "insert",
    "update",
    "delete",
    "replace",
    "create",
    "drop",
    "alter",
    "truncate",
)


def check_sql_has_data_changes(sql_query: str):
    """Проверяет, является ли sql-запрос изменяющим данные бд."""

    first_word_in_query = sql_query.strip().lower().split()[0]
    if first_word_in_query in WRITE_COMMANDS:
        logger.warning("Запрос является дата изменяющим. Запрос: %s", sql_query)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="SQL-запрос не должен изменять данные.",
        )


def execute_sql(sql_query: str, db_type: DBType):
    """Проверяет какой тип бд и передает исполнение соответствующему исполнителю."""

    check_sql_has_data_changes(sql_query)

    if db_type == DBType.sqlite:
        result = execute_sqlite_query(sql_query)
    elif db_type == DBType.vertica:
        result = execute_vertica_query(sql_query)
    else:
        logger.warning("Пользователь указал несуществующий тип бд: %s", db_type)
        raise ValueError(f"Неподдерживаемый тип БД: {db_type}")

    return result
