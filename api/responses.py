from starlette.status import (HTTP_400_BAD_REQUEST,
                              HTTP_422_UNPROCESSABLE_ENTITY)


def generate_response(description: str, detail: str):
    return {
        "description": description,
        "content": {"application/json": {"example": {"detail": detail}}},
    }


incorrect_sql_query = generate_response(
    description="Некорректный SQL-запрос.",
    detail="LLM сгенерировала некорректный SQL-запрос.",
)

data_change_query = generate_response(
    description="SQL-запрос изменяет данные.",
    detail="SQL-запрос не должен изменять данные.",
)

ask_responses = {
    HTTP_400_BAD_REQUEST: incorrect_sql_query,
    HTTP_422_UNPROCESSABLE_ENTITY: data_change_query,
}
