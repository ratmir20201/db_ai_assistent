import json
from typing import List

import vertica_python
from langchain_core.documents import Document

from db_parsing.test_db_schema import mock_data


def parse_vertica_to_documents() -> List[Document]:
    # with vertica_python.connect(**settings.vertica.conn_info) as connection:
    # cursor = connection.cursor()
    # cursor.execute(
    #     """
    #     SELECT
    #       tab.table_schema,
    #       tab.table_name,
    #       tab_com.COMMENT table_comment,
    #       col.column_name,
    #       col.data_type,
    #       col_com.COMMENT column_comment
    #     FROM v_catalog.tables tab
    #     JOIN v_catalog.columns col
    #       ON tab.table_id = col.table_id
    #     LEFT JOIN v_catalog.comments col_com
    #       ON tab.table_id = col_com.object_id
    #       AND col.column_name = col_com.child_object
    #     LEFT JOIN v_catalog.comments tab_com
    #       ON tab.table_id = tab_com.object_id
    #       AND tab_com.child_object = ''
    #     WHERE tab.table_schema IN (/*'SANDBOX',*/ 'DWH', 'STAGE_DO', 'DM')
    #     ORDER BY tab.table_schema_id, tab.table_id, col.ordinal_position
    #     """
    # )
    # rows = cursor.fetchall()
    # # Group data by (schema, table_name)
    # tables = defaultdict(
    #     lambda: {"schema": "", "table": "", "table_comment": "", "columns": []}
    # )
    #
    # for row in rows:
    #     (
    #         schema,
    #         table_name,
    #         table_comment,
    #         column_name,
    #         column_type,
    #         column_comment,
    #     ) = row
    #
    #     key = (schema, table_name)
    #     table_doc = tables[key]
    #
    #     table_doc["schema"] = schema
    #     table_doc["table"] = table_name
    #     table_doc["table_comment"] = table_comment
    #     table_doc["columns"].append(
    #         {"name": column_name, "type": column_type, "comment": column_comment}
    #     )

    # Convert to list of documents
    # rag_documents = list(tables.values())

    # return rag_documents

    documents = []
    for table in mock_data:
        content = json.dumps(table, ensure_ascii=False)
        documents.append(Document(page_content=content))

    return documents
