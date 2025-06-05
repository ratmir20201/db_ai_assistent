from langchain_ollama import ChatOllama
from langchain_ollama import OllamaLLM

from llms.base_llm import BaseLLM
from llms.prompts import (
    VerticaPrompt,
    SQLitePrompt,
)
from schemas import DBType


class DeepseekR1LLM(BaseLLM):
    """Класс для работы с deepseek-r1."""

    llm = ChatOllama(model="deepseek-r1:latest", temperature=0.1, num_ctx=8192)
    db_type_prompt_class = {
        DBType.vertica: VerticaPrompt(),
        DBType.sqlite: SQLitePrompt(),
    }
