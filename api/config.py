from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

current_dir = Path(__file__).resolve().parent


class LLMSettings(BaseSettings):
    """Настройки LLM."""

    host: str = ""
    model: str = ""

    class Config:
        env_prefix = "LLM__"


class ParsingSettings(BaseSettings):
    """Настройки для парсинга."""

    db_path: str = ""

    @property
    def absolute_db_path(self):
        return current_dir / self.db_path

    class Config:
        env_prefix = "PARSE__"


class RedisSettings(BaseSettings):
    """Настройки Redis."""

    host: str = "localhost"
    port: int = 6379
    db: int = 0

    class Config:
        env_prefix = "REDIS__"


class Settings(BaseSettings):
    """Общие настройки приложения."""

    llm: LLMSettings = LLMSettings()
    parse: ParsingSettings = ParsingSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
