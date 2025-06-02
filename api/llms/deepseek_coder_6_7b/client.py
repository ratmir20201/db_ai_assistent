from langchain_ollama import ChatOllama
from langchain_ollama import OllamaLLM

from llms.base_llm import BaseLLM
from llms.prompts import (
    VerticaPrompt,
    SQLitePrompt,
)
from schemas import DBType


class DeepseekCoderV2LLM(BaseLLM):
    """Класс для работы с deepseek-coder:6.7b."""

    llm = ChatOllama(model="deepseek-coder:6.7b", temperature=0.2)
    db_type_prompt_class = {
        DBType.vertica: VerticaPrompt(),
        DBType.sqlite: SQLitePrompt(),
    }
