from langchain_ollama import OllamaLLM

from llms.base_llm import BaseLLM
from llms.mistral.prompts import (
    MistralVerticaPrompt,
    MistralSQLitePrompt,
)
from logger import logger
from redis_history import history
from schemas import DBType


class MistralLLM(BaseLLM):
    """Класс для работы с mistral."""

    llm = OllamaLLM(model="mistral:latest", temperature=0.2)
    db_type_prompt_class = {
        DBType.vertica: MistralVerticaPrompt(),
        DBType.sqlite: MistralSQLitePrompt(),
    }

    def llm_chatting(self) -> tuple[str, str] | str:
        """
        Отправляет текстовый запрос в Ollama и возвращает ответ пользователю.

        Если параметр sql_required=True функция вернет SQL-запрос с объяснением,
        иначе будет возвращен простой ответ на вопрос.
        Сохраняет запрос пользователя и ответ llm в redis.
        """

        logger.debug("Запрос пользователя: %s", self.question)

        history.add_user_message(self.question)

        if not self.sql_required:
            return self._get_response_to_general_prompt()
        else:
            sql_response = self._get_response_to_sql_prompt()
            try:
                sql_query, explanation = sql_response.split("|||")
            except ValueError:
                logger.warning(
                    "Ответ LLM не содержит разделителей |||: %s", sql_response
                )
                return sql_response
            return sql_query, explanation

    def _get_response_to_general_prompt(self) -> str:
        prompt = self.build_basic_prompt()
        chain = prompt | self.llm
        response = chain.invoke({})
        history.add_ai_message(response)

        logger.debug("Ответ LLM: %s", response)

        return response

    def _get_response_to_sql_prompt(self) -> str:
        prompt = self.build_sql_prompt()
        chain = prompt | self.llm
        response = chain.invoke({})
        history.add_ai_message(response)

        logger.debug("Ответ LLM c sql-запросом: %s", response)

        return response
