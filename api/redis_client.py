import json
from typing import Literal

import redis
from config import settings
from logger import logger

REDIS_CHAT_KEY = "chat_history"

redis_client = redis.Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    db=settings.redis.db,
    decode_responses=True,
)


RoleType = Literal["user", "assistant"]


def add_message_to_redis(role: RoleType, message: str):
    """Сохраняет ответ пользователя или llm в redis."""
    redis_client.rpush(
        REDIS_CHAT_KEY,
        json.dumps({"role": role, "content": message}),
    )
    logger.debug("Сообщение сохранено в redis. Role: %s. Message: %s.", role, message)


def get_message_from_redis() -> list[dict[str, str]]:
    """Возвращает историю сообщений из redis."""
    chat_history = redis_client.lrange(REDIS_CHAT_KEY, 0, -1)
    history_messages = [json.loads(msg) for msg in chat_history]

    return history_messages
