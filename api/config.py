from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

current_dir = Path(__file__).resolve().parent
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "frontend"


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

    @property
    def async_db_url(self) -> str:
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}".format(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            name=self.name,
        )

    class Config:
        env_prefix = "DB__"


class AccessTokenSettings(BaseSettings):
    """Настройки токена для аутентификации."""

    lifetime_seconds: int = 3600  # Кол-во секунд которое хранится токен
    reset_password_token_secret: str = ""
    verification_token_secret: str = ""

    class Config:
        env_prefix = "ACCESS_TOKEN__"


class ApiSettings(BaseSettings):
    """Настройки api сервера."""

    superuser_name: str = "admin"
    superuser_email: str = "admin@admin.com"
    superuser_password: str = "admin"

    class Config:
        env_prefix = "API__"


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

    # parse: ParsingSettings = ParsingSettings()
    redis: RedisSettings = RedisSettings()
    api: ApiSettings = ApiSettings()
    access_token: AccessTokenSettings = AccessTokenSettings()
    vertica: VerticaSettings = VerticaSettings()
    db: DbSettings = DbSettings()


settings = Settings()
