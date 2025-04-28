from starlette.status import HTTP_400_BAD_REQUEST


def generate_response(description: str, detail: str):
    return {
        "description": description,
        "content": {"application/json": {"example": {"detail": detail}}},
    }


incorrect_sql_query = generate_response(
    description="Некорректный SQL-запрос.",
    detail="LLM сгенерировала некорректный SQL-запрос.",
)

ask_responses = {HTTP_400_BAD_REQUEST: incorrect_sql_query}
