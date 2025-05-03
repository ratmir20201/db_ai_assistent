from schemas import DBType
from sql_executors.sqlite_runner import execute_sqlite_query
from sql_executors.vertica_runner import execute_vertica_query


def execute_sql(sql_query: str, db_type: DBType):
    """Проверяет какой тип бд и передает исполнение соответствующему исполнителю."""

    if db_type == DBType.sqlite:
        result = execute_sqlite_query(sql_query)
    elif db_type == DBType.vertica:
        result = execute_vertica_query(sql_query)
    else:
        raise ValueError(f"Неподдерживаемый тип БД: {db_type}")

    return result
