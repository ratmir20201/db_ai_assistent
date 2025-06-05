from typing import List

import vertica_python
from langchain_core.documents import Document

from config import settings
from db_parsing.test_db_schema import mock_data
from utils.check_table import is_backup_table


def parse_vertica_to_documents() -> List[Document]:
    with vertica_python.connect(**settings.vertica.conn_info) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
              tab.table_schema,
              tab.table_name,
              tab_com.COMMENT table_comment,
              col.column_name,
              col.data_type,
              col_com.COMMENT column_comment
            FROM v_catalog.tables tab
            JOIN v_catalog.columns col
              ON tab.table_id = col.table_id
            LEFT JOIN v_catalog.comments col_com
              ON tab.table_id = col_com.object_id
              AND col.column_name = col_com.child_object
            LEFT JOIN v_catalog.comments tab_com
              ON tab.table_id = tab_com.object_id
              AND tab_com.child_object = ''
           -- WHERE tab.table_schema IN (/*'SANDBOX',*/ 'DWH', 'STAGE_DO', 'DM')
            WHERE tab.table_schema IN (/*'SANDBOX',*/ 'DWH', 'DM')
            ORDER BY tab.table_schema_id, tab.table_id, col.ordinal_position
            """
        )
        rows = cursor.fetchall()
        documents = []

        for row in rows:
            (
                schema,
                table_name,
                table_comment,
                column_name,
                column_type,
                column_comment,
            ) = row

            if is_backup_table(table_name):
                continue

            text = " ".join(str(item) for item in row)
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "schema": schema,
                        "table_name": table_name,
                        "table_comment": table_comment,
                    },
                )
            )

        return documents

    # documents = []
    #
    # for table in mock_data:
    #     content_lines = [f"Схема: {table['schema']}", f"Таблица: {table['table']}"]
    #     if table["table_comment"]:
    #         content_lines.append(f"Комментарий: {table['table_comment']}")
    #     content_lines.append("Колонки:")
    #     for col in table["columns"]:
    #         content_lines.append(f"  - {col['name']} ({col['type']}): {col['comment']}")
    #
    #     content = "\n".join(content_lines)
    #     metadata = {"schema": table["schema"], "table": table["table"]}
    #
    #     documents.append(Document(page_content=content, metadata=metadata))
    #
    # return documents


if __name__ == "__main__":
    print(parse_vertica_to_documents())
