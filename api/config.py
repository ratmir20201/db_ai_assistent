from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class LLMSettings(BaseSettings):
    """Настройки LLM."""

    class Config:
        env_prefix = "LLM__"


class Settings(BaseSettings):
    """Общие настройки приложения."""

    open_ai: LLMSettings = LLMSettings()


settings = Settings()
