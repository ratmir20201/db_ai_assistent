from collections import defaultdict
from typing import List, Dict

import vertica_python
from langchain_core.documents import Document

from config import settings
from utils.check_table import is_backup_table


def parse_vertica_to_documents(columns_per_chunk: int = 10) -> List[Document]:
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
        tables: Dict[tuple, List[str]] = defaultdict(list)

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

            key = (schema, table_name, table_comment)
            # Каждая строка — просто набор значений через пробел
            column = f"{column_name} {column_type} {column_comment}"
            tables[key].append(column)

        for (schema, table_name, table_comment), columns in tables.items():
            for i in range(0, len(columns), columns_per_chunk):
                chunk = columns[i : i + columns_per_chunk]
                text = " ".join(
                    [
                        f"schema: {schema}",
                        f"table_name: {table_name}",
                        table_comment or "",
                    ]
                    + chunk
                )
                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "schema": schema,
                            "table_name": table_name,
                            "table_comment": table_comment,
                            "chunk_index": i // columns_per_chunk,
                        },
                    )
                )

        return documents


if __name__ == "__main__":
    print(parse_vertica_to_documents(10))
