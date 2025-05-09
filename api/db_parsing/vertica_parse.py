import vertica_python
from config import settings


def parse_vertica_to_json():
    with vertica_python.connect(**settings.vertica.conn_info) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT table_schema, table_name
            FROM v_catalog.tables
            WHERE table_schema NOT IN ('v_internal', 'v_catalog')
            """
        )
        tables = cursor.fetchall()
        schema: dict[str, dict | list] = {"tables": {}}

        for i_schema, i_table in tables:
            full_table_name = f"{i_schema}.{i_table}"
            cursor.execute(
                f"""
                SELECT column_name, data_type, is_nullable
                FROM v_catalog.columns
                WHERE table_schema = '{i_schema}' AND table_name = '{i_table}'
                """
            )
            columns = cursor.fetchall()
            table_columns = []
            for column_name, data_type, nullable in columns:
                table_columns.append(column_name)
            schema["tables"][full_table_name] = table_columns

        return schema
