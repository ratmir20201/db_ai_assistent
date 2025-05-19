from starlette.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


def generate_response(description: str, detail: str):
    return {
        "description": description,
        "content": {"application/json": {"example": {"detail": detail}}},
    }


def generate_responses(description: str, examples: dict[str, dict]):
    return {
        "description": description,
        "content": {"application/json": {"examples": examples}},
    }


incorrect_sql_query = generate_response(
    description="Внутренняя ошибка: некорректный SQL от LLM.",
    detail="LLM сгенерировала некорректный SQL-запрос. Попробуйте позже.",
)

data_change_query_response = {
    "summary": "SQL-запрос изменяет данные",
    "value": {"detail": "SQL-запрос не должен изменять данные."},
}

invalid_enum_response = {
    "summary": "Неверный тип db_type или llm_type",
    "value": {
        "detail": "Значение не является действительным членом enum; разрешено: 'sqlite', 'vertica'"
    },
}

bad_data = generate_responses(
    description="Ошибка обработки данных.",
    examples={
        "data_change": data_change_query_response,
        "invalid_enum": invalid_enum_response,
    },
)

ask_responses = {
    HTTP_422_UNPROCESSABLE_ENTITY: bad_data,
    HTTP_500_INTERNAL_SERVER_ERROR: incorrect_sql_query,
}
