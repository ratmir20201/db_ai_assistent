import sqlite3


def execute_sql(sql_query: str):
    with sqlite3.connect("../db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        return result
