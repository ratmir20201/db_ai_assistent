import sqlite3


def execute_sql(sql_query: str):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    conn.close()
    return result
