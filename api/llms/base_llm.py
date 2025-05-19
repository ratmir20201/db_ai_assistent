from abc import ABC, abstractmethod
from typing import Type

from langchain_core.prompts import ChatPromptTemplate

from llms.base_prompt import BasePrompt
from redis_history import history
from schemas import DBType


class BaseLLM(ABC):
    llm = ...
    db_type_prompt_class: dict[DBType, Type[BasePrompt]] = {}

    def __init__(self, question: str, db_type: DBType, sql_required: bool):
        self.question = question
        self.db_type = db_type
        self.sql_required = sql_required

    @abstractmethod
    def llm_chatting(self) -> tuple[str, str] | str:
        """Основной метод в котором ведется диалог пользователя с ассистентом."""

    def build_sql_prompt(self):
        """Получает и отдает промпт с sql-запросом для llm."""

        if self.db_type in self.db_type_prompt_class.keys():
            system_prompt = self.db_type_prompt_class[self.db_type].get_sql_prompt()
            return self._get_chat_prompt_dialog(system_prompt)

        raise TypeError(f"Неподдерживаемый тип БД: {self.db_type}")

    def build_basic_prompt(self):
        """Получает и отдает базовый промпт для llm."""

        if self.db_type in self.db_type_prompt_class.keys():
            system_prompt = self.db_type_prompt_class[self.db_type].get_basic_prompt()
            return self._get_chat_prompt_dialog(system_prompt)

        raise TypeError(f"Неподдерживаемый тип БД: {self.db_type}")

    def _get_chat_prompt_dialog(self, system_prompt: str):
        """Возвращает историю диалога пользователя с ассистентом."""
        return ChatPromptTemplate.from_messages(
            [("system", system_prompt), *history.messages, ("human", self.question)]
        )
