from itertools import chain

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

        if "v_catalog.foreign_keys" in sql_query:
            tables = [f"{table_info[1]}.{table_info[2]}" for table_info in result]
            return tables

        if "v_catalog.columns" in sql_query:
            columns = list(chain.from_iterable(result))
            return columns

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
