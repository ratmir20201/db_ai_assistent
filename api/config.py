from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

current_dir = Path(__file__).resolve().parent


class LLMSettings(BaseSettings):
    """Настройки LLM."""

    host: str = "http://localhost"
    port: str = "11434"
    model: str = "mistral:latest"

    class Config:
        env_prefix = "LLM__"


# class ParsingSettings(BaseSettings):
#     """Настройки для парсинга."""
#
#     db_path: str = ""
#
#     @property
#     def absolute_db_path(self):
#         return current_dir / self.db_path
#
#     class Config:
#         env_prefix = "PARSE__"


class DbSettings(BaseSettings):
    """Настройки базы данных."""

    user: str = "user"
    password: str = "password"
    host: str = "postgres"
    port: int = 5432
    name: str = ""
    echo: bool = False

    @property
    def db_url(self) -> str:
        return "postgresql+psycopg://{user}:{password}@{host}:{port}/{name}".format(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            name=self.name,
        )

    class Config:
        env_prefix = "DB__"


class VerticaSettings(BaseSettings):
    """Настройки базы данных."""

    user: str = "user"
    password: str = "password"
    host: str = "localhost"
    port: int = 5433
    database: str = ""

    @property
    def conn_info(self) -> dict:
        return {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.database,
        }

    class Config:
        env_prefix = "VERTICA__"


class RedisSettings(BaseSettings):
    """Настройки Redis."""

    host: str = "localhost"
    port: int = 6379
    db: int = 0

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"

    class Config:
        env_prefix = "REDIS__"


class Settings(BaseSettings):
    """Общие настройки приложения."""

    llm: LLMSettings = LLMSettings()
    # parse: ParsingSettings = ParsingSettings()
    redis: RedisSettings = RedisSettings()
    vertica: VerticaSettings = VerticaSettings()
    db: DbSettings = DbSettings()


settings = Settings()
