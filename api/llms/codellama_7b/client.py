from langchain_ollama import ChatOllama
from langchain_ollama import OllamaLLM

from llms.base_llm import BaseLLM
from llms.prompts import (
    VerticaPrompt,
    SQLitePrompt,
)
from schemas import DBType


class Codellama7bLLM(BaseLLM):
    """Класс для работы с codellama:7b."""

    llm = ChatOllama(model="codellama:7b", temperature=0.2)
    db_type_prompt_class = {
        DBType.vertica: VerticaPrompt(),
        DBType.sqlite: SQLitePrompt(),
    }
