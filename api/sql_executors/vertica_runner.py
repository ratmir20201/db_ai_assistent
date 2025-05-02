import vertica_python
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from config import settings
from logger import logger


def execute_vertica_query(sql_query: str) -> list:
    """Проверяет vertica-запрос на валидность и исполняет его."""
    with vertica_python.connect(**settings.vertica.conn_info) as connection:
        is_validate = validate_vertica_query(sql_query, connection)
        if not is_validate:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="LLM сгенерировала некорректный SQL-запрос.",
            )

        cursor = connection.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()

        return result


def validate_vertica_query(
    sql_query: str,
    connection: vertica_python.Connection,
) -> bool:
    """Проверяет sql-запрос исполняя его и откатываясь."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"EXPLAIN {sql_query}")
        cursor.fetchall()
        return True
    except Exception as e:
        logger.error("Ошибка синтаксиса SQL в Vertica: %s", e)
        return False
