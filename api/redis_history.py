from langchain_community.chat_message_histories import RedisChatMessageHistory

from config import settings

history = RedisChatMessageHistory(
    session_id="user_123",  # TODO: здесь нужен либо user_id либо session_id
    url=settings.redis.url,
)
