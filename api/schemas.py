from pydantic import BaseModel


class UserRequest(BaseModel):
    """Схема пользовательского ввода."""

    question: str


class AssistentResponse(BaseModel):
    """Схема ответа."""

    sql_query: str
    result: list
