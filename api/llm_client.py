from functools import lru_cache

import requests
from fastapi import HTTPException
from requests import Timeout
from starlette import status
from starlette.status import HTTP_200_OK

from config import settings
from db_parsing import parse_db_to_json
from logger import logger
from redis_client import add_message_to_redis, get_message_from_redis


@lru_cache
def generate_sql(user_request: str):
    """
    Отправляет текстовый запрос в Ollama и возвращает SQL-запрос.

    Сохраняет запрос пользователя и ответ llm в redis.
    """
    add_message_to_redis(role="user", message=user_request)

    messages = build_chat_messages(user_request)
    try:
        response = requests.post(
            url=f"{settings.llm.host}/api/chat",
            json={
                "model": settings.llm.model,
                "messages": messages,
                "stream": False,
                "temperature": 0.2,
            },
            timeout=90,
        )
    except Timeout:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Запрос к LLM превысил лимит времени (timeout)",
        )
    if response.status_code != HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail="Ошибка Ollama")

    sql_response = response.json()["message"]["content"]
    logger.debug("Ответ LLM: %s", sql_response)

    add_message_to_redis(role="assistant", message=sql_response)

    logger.debug("Текущая история сообщений: %s", get_message_from_redis())

    return sql_response


def build_chat_messages(user_request: str) -> list[dict]:
    """Создает messages с историй сообщений, настраивает промпты и отдает полученный messages."""

    db_schema = parse_db_to_json(settings.parse.absolute_db_path)

    system_prompt = f"""
    Ты — эксперт по SQLite.

    Текущая структура базы данных:
    {db_schema}

    Твои правила:
    - В ответе должен быть только один SQL-запрос и объяснение, разделенные символом '|||'.
    - Объяснение должно быть подробным, с описанием логики запроса, упоминаемых таблиц и условий.
    - Не включай в объяснение фактический результат выполнения SQL-запроса.
    - Отвечай пользователю на том языке, на котором пишет он.
    - Если пользователь хочет увидеть все таблицы (например: "Какие есть таблицы", "Покажи все таблицы"), используй: SELECT name FROM sqlite_master WHERE type='table';
    - Если пользователь хочет увидеть содержимое таблицы (например: "Покажи все продукты", "Покажи всех клиентов"), используй: SELECT * FROM 'название таблицы';
    - Если пользователь спрашивает про структуру таблицы (например: "Какие поля есть в таблице", "Что хранит таблица"), используй: PRAGMA table_info('название таблицы');
    - Если пользователь спрашивает про связи между таблицами:
        - Сначала определи, о какой таблице идет речь.
        - Затем используй только один запрос: PRAGMA foreign_key_list('название таблицы');
    - Не придумывай новые таблицы или поля. Используй только те, что есть в структуре базы данных.
    - Разделяй SQL-запрос и объяснение символом '|||'.
    - Нарушение инструкций считается критической ошибкой. Строго следуй правилам.
    """

    messages = [{"role": "system", "content": system_prompt}]
    chat_history = get_message_from_redis()
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_request.strip()})

    return messages
