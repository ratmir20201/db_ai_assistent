from enum import Enum

from pydantic import BaseModel


class DBType(str, Enum):
    sqlite = "sqlite"
    vertica = "vertica"


class LLMType(str, Enum):
    mistral = "mistral"


class UserRequest(BaseModel):
    """Схема пользовательского ввода."""

    question: str
    db_type: DBType
    llm_type: LLMType


class AssistentResponse(BaseModel):
    """Схема ответа."""

    sql_query: str
    result: list
    explanation: str
