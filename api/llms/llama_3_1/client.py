from langchain_ollama import ChatOllama
from langchain_ollama import OllamaLLM

from llms.base_llm import BaseLLM
from llms.prompts import (
    VerticaPrompt,
    SQLitePrompt,
)
from schemas import DBType


class Llama31LLM(BaseLLM):
    """Класс для работы с llama3.1:latest."""

    llm = ChatOllama(model="llama3.1:latest", temperature=0.1)
    db_type_prompt_class = {
        DBType.vertica: VerticaPrompt(),
        DBType.sqlite: SQLitePrompt(),
    }
