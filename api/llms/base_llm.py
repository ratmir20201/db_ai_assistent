from abc import ABC
from typing import Type

from langchain_core.prompts import ChatPromptTemplate

# from db_parsing.sqlite_parse import parse_sqlite_to_json
from db_parsing.vertica_parse import parse_vertica_to_documents
from llms.base_prompt import BasePrompt
from llms.embeddings import vectorstore
from logger import logger
from redis_history import history
from schemas import DBType


class BaseLLM(ABC):
    llm = ...
    db_type_prompt_class: dict[DBType, Type[BasePrompt]] = {}
    db_type_db_parse: dict[DBType, list | dict] = {
        # DBType.sqlite: parse_sqlite_to_json(),
        DBType.vertica: parse_vertica_to_documents(),
    }

    def __init__(self, question: str, db_type: DBType, sql_required: bool):
        self.question = question
        self.db_type = db_type
        self.sql_required = sql_required

    def llm_chatting(self) -> tuple[str, str] | str:
        """
        Основной метод в котором ведется диалог пользователя с ассистентом.

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

    def _build_sql_prompt(self) -> ChatPromptTemplate:
        """Получает и отдает промпт с sql-запросом для llm."""

        if self.db_type in self.db_type_prompt_class.keys():
            system_prompt = self.db_type_prompt_class[self.db_type].get_sql_prompt()
            return self._get_chat_prompt_dialog(system_prompt)

        raise TypeError(f"Неподдерживаемый тип БД: {self.db_type}")

    def _build_basic_prompt(self) -> ChatPromptTemplate:
        """Получает и отдает базовый промпт для llm."""

        if self.db_type in self.db_type_prompt_class.keys():
            system_prompt = self.db_type_prompt_class[self.db_type].get_basic_prompt()
            return self._get_chat_prompt_dialog(system_prompt)

        raise TypeError(f"Неподдерживаемый тип БД: {self.db_type}")

    def _make_chain(self, prompt: ChatPromptTemplate) -> str:
        """Создает цепь, и делает запрос в llm передавая неполную схему бд."""

        chain = prompt | self.llm
        incomplete_schema = vectorstore.similarity_search(self.question, 50)
        formatted_schema = "\n\n".join(doc.page_content for doc in incomplete_schema)
        response = chain.invoke({"schema": formatted_schema})
        history.add_ai_message(response)

        return response

    def _get_response_to_general_prompt(self) -> str:
        prompt = self._build_basic_prompt()
        response = self._make_chain(prompt)

        logger.debug("Ответ LLM: %s", response)

        return response

    def _get_response_to_sql_prompt(self) -> str:
        prompt = self._build_sql_prompt()
        response = self._make_chain(prompt)

        logger.debug("Ответ LLM c sql-запросом: %s", response)

        return response

    @staticmethod
    def _get_chat_prompt_dialog(system_prompt: str) -> ChatPromptTemplate:
        """Возвращает историю диалога пользователя с ассистентом."""

        logger.debug("История сообщений: %s", history.messages)
        return ChatPromptTemplate.from_messages(
            [("system", system_prompt), *history.messages]
        )
