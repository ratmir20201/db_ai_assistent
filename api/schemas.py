from enum import Enum

from fastapi_users import schemas
from pydantic import BaseModel


class DBType(str, Enum):
    sqlite = "sqlite"
    vertica = "vertica"


class LLMType(str, Enum):
    mistral = "mistral"
    deepseek_r1 = "deepseek_r1"
    deepseek_coder_v1 = "deepseek-coder:1.3b"
    deepseek_coder_v2 = "deepseek-coder:6.7b"
    llama31 = "llama:3.1"
    llama32 = "llama:3.2"
    codellama_7b = "codellama:7b"


class UserRequest(BaseModel):
    """Схема пользовательского ввода."""

    question: str
    db_type: DBType
    llm_type: LLMType
    sql_required: bool = False


class AssistentResponse(BaseModel):
    """Схема ответа."""

    sql_query: str
    sql_script_result: list[list[str]] | str
    explanation: str
    message_id: int


class UserRead(schemas.BaseUser[int]):
    """Схема для чтения пользователя."""

    username: str


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания пользователя."""

    username: str
    password: str


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для изменения пользователя."""

    username: str
