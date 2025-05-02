from functools import lru_cache

import requests
from fastapi import HTTPException
from requests import Timeout
from starlette import status
from starlette.status import HTTP_200_OK

from config import settings
from llm_clients.mistral.prompts import get_sqlite_prompt
from logger import logger
from redis_client import add_message_to_redis, get_message_from_redis
from schemas import DBType


@lru_cache
def generate_sql(user_request: str, db_type: DBType):
    """
    Отправляет текстовый запрос в Ollama и возвращает SQL-запрос.

    Сохраняет запрос пользователя и ответ llm в redis.
    """
    add_message_to_redis(role="user", message=user_request)

    messages = build_chat_messages(user_request, db_type)
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


def build_chat_messages(user_request: str, db_type: DBType) -> list[dict]:
    """Создает messages с историей сообщений, настраивает промпты и отдает полученный messages."""

    if db_type == DBType.sqlite:
        system_prompt = get_sqlite_prompt()
    elif db_type == DBType.vertica:
        system_prompt = ""
    else:
        raise ValueError(f"Неподдерживаемый тип БД: {db_type}")

    messages = [{"role": "system", "content": system_prompt}]
    chat_history = get_message_from_redis()
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_request.strip()})

    return messages
