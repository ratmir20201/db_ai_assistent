from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class LLMSettings(BaseSettings):
    """Настройки LLM."""

    host: str = ""
    model: str = ""

    class Config:
        env_prefix = "LLM__"


class Settings(BaseSettings):
    """Общие настройки приложения."""

    llm: LLMSettings = LLMSettings()


settings = Settings()
