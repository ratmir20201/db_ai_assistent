from abc import ABC
from typing import Type, List

from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# from db_parsing.sqlite_parse import parse_sqlite_to_json
from db_parsing.vertica_parse import parse_vertica_to_documents
from llms.base_prompt import BasePrompt
from llms.embeddings import vectorstore
from logger import logger
from schemas import DBType
from translator import Translator


def format_table_schema(docs: List[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


class BaseLLM(ABC):
    llm = ...
    db_type_prompt_class: dict[DBType, Type[BasePrompt]] = {}
    db_type_db_parse: dict[DBType, list | dict] = {
        # DBType.sqlite: parse_sqlite_to_json(),
        DBType.vertica: parse_vertica_to_documents(),
    }

    def __init__(
        self,
        question: str,
        db_type: DBType,
        sql_required: bool,
        history: RedisChatMessageHistory,
    ):
        self.question = question
        self.db_type = db_type
        self.sql_required = sql_required
        self.history = history
        self.was_translated: bool = False
        self.translated_user_question: str | None = None

    def get_llm_response(self) -> tuple[str, str] | str:
        """
        Основной метод в котором ведется диалог пользователя с ассистентом.

        Отправляет текстовый запрос в Ollama и возвращает ответ пользователю.

        Если параметр sql_required=True функция вернет SQL-запрос с объяснением,
        иначе будет возвращен простой ответ на вопрос.
        Сохраняет запрос пользователя и ответ llm в redis.
        """
        logger.debug("Запрос пользователя: %s", self.question)

        self._add_english_user_message_to_history()

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

    def _add_english_user_message_to_history(self):
        language = Translator.language_detect(self.question)
        if language == "ru":
            user_message = Translator.translate_from_russian_into_english(self.question)
            self.history.add_user_message(user_message)
            self.was_translated = True
            self.translated_user_question = user_message
        else:
            self.history.add_user_message(self.question)

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

        chain = {"schema": format_table_schema} | prompt | self.llm | StrOutputParser()
        if self.was_translated:
            incomplete_schema = vectorstore.similarity_search(
                self.translated_user_question, 50
            )
        else:
            incomplete_schema = vectorstore.similarity_search(self.question, 50)
        response = chain.invoke(incomplete_schema)
        self.history.add_ai_message(response)

        return response

    def _get_response_to_general_prompt(self) -> str:
        prompt = self._build_basic_prompt()
        response = self._make_chain(prompt)

        logger.debug("Ответ LLM: %s", response)
        if self.was_translated:
            response_in_user_lang = Translator.translate_from_english_into_russian(
                response
            )
            return response_in_user_lang

        return response

    def _get_response_to_sql_prompt(self) -> str:
        prompt = self._build_sql_prompt()
        response = self._make_chain(prompt)

        logger.debug("Ответ LLM c sql-запросом: %s", response)
        if self.was_translated:
            response_in_user_lang = Translator.translate_from_english_into_russian(
                response
            )
            return response_in_user_lang

        return response

    def _get_chat_prompt_dialog(self, system_prompt: str) -> ChatPromptTemplate:
        """Возвращает историю диалога пользователя с ассистентом."""

        logger.debug("История сообщений: %s", self.history.messages)
        return ChatPromptTemplate.from_messages(
            [("system", system_prompt), *self.history.messages]
        )
