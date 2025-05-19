from abc import ABC, abstractmethod


class BasePrompt(ABC):

    @abstractmethod
    def get_sql_prompt(self) -> str:
        """Возвращает sql-промпт."""

    @abstractmethod
    def get_basic_prompt(self) -> str:
        """Возвращает базовый промпт."""
