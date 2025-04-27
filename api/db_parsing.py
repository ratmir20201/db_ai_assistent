import sqlite3


def parse_db_to_json(db_path: str) -> dict[str, dict[str, list]]:
    """Парсит бд по указанному пути в json."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        schema = {"tables": {}, "foreign_keys": []}

        for (table_name,) in tables:
            if table_name.startswith("sqlite_") or table_name.startswith("django_"):
                continue
            cursor.execute(f"PRAGMA table_info('{table_name}')")
            table_info = cursor.fetchall()
            columns_name = [column[1] for column in table_info]
            schema["tables"][table_name] = columns_name

            cursor.execute(f"PRAGMA foreign_key_list('{table_name}')")
            foreign_key_info = cursor.fetchall()

            for fk in foreign_key_info:
                schema["foreign_keys"].append(
                    {
                        "from_table": table_name,
                        "from_column": fk[3],  # локальная колонка
                        "to_table": fk[2],  # таблица, на которую идет ссылка
                        "to_column": fk[4],  # колонка в другой таблице
                    }
                )

        return schema
