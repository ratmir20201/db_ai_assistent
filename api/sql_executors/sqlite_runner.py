import sqlite3

from config import settings
from fastapi import HTTPException
from logger import logger
from starlette.status import HTTP_400_BAD_REQUEST


def execute_sqlite_query(sql_query: str) -> list:
    """Проверяет sqlite-запрос на валидность и исполняет его."""

    with sqlite3.connect(settings.parse.absolute_db_path) as conn:
        is_validate = validate_sqlite_query(sql_query, conn)
        if not is_validate:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="LLM сгенерировала некорректный SQL-запрос.",
            )

        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        if sql_query.startswith("PRAGMA foreign_key_list"):
            table_names = [row[2] for row in result]
            return table_names

        if sql_query.startswith("PRAGMA table_info"):
            column_names = [column[1] for column in result]
            return column_names

        return result


def validate_sqlite_query(sql_query: str, connection: sqlite3.Connection) -> bool:
    """Проверяет sql-запрос исполняя его и откатываясь."""
    try:
        cursor = connection.cursor()
        cursor.execute("SAVEPOINT validate;")
        cursor.execute(sql_query)
        cursor.execute("ROLLBACK TO validate;")
        return True
    except sqlite3.Error as e:
        logger.error("Ошибка синтаксиса SQL в sqlite: %s", e)
        return False
