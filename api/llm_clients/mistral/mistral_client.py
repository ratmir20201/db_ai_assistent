from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate

from config import settings
from llm_clients.mistral.prompts import (
    get_classic_vertica_prompt,
    get_sqlite_prompt,
    get_vertica_prompt,
)
from logger import logger
from redis_history import history
from schemas import DBType


def generate_sql(user_request: str, db_type: DBType) -> tuple[str, str]:
    """
    Отправляет текстовый запрос в Ollama и возвращает SQL-запрос с объяснением.

    Сохраняет запрос пользователя и ответ llm в redis.
    """
    history.add_user_message(user_request)

    llm = Ollama(model=settings.llm.model, temperature=0.2)
    prompt = build_prompt(user_request, db_type)
    chain = prompt | llm
    response = chain.invoke()

    logger.debug("Запрос пользователя: %s", user_request)
    logger.debug("Ответ LLM: %s", response)

    history.add_ai_message(response)

    logger.debug("Текущая история сообщений: %s", history.messages)

    try:
        sql_query, explanation = response.split("|||")
    except ValueError:
        return response.strip(), ""

    return sql_query, explanation


def build_prompt(user_request: str, db_type: DBType):
    """Создает messages с историей сообщений, настраивает промпты и отдает полученный messages."""

    if db_type == DBType.sqlite:
        system_prompt = get_sqlite_prompt()
    elif db_type == DBType.vertica:
        system_prompt = check_get_vertica_semantic(user_request)
    else:
        raise ValueError(f"Неподдерживаемый тип БД: {db_type}")

    prompt = ChatPromptTemplate.from_messages(
        [("system", system_prompt), *history.messages, ("human", user_request)]
    )

    return prompt


def check_get_vertica_semantic(user_request: str) -> str:
    # Примитивная эвристика, можно заменить на классификацию или emb-сопоставление
    is_usual_question = any(
        word in user_request.lower()
        for word in ["где", "наход", "лежат", "содержат", "сохраня"]
    )

    if is_usual_question:
        return get_classic_vertica_prompt()

    return get_vertica_prompt()
