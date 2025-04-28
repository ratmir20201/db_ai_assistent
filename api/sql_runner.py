import sqlite3


def execute_sql(sql_query: str):
    with sqlite3.connect("../db.sqlite3") as conn:
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
