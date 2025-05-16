from langchain.output_parsers import BooleanOutputParser
from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

from config import settings
from llm_clients.mistral.prompts import (
    get_sqlite_prompt,
    get_vertica_prompt,
    get_general_vertica_prompt,
)
from logger import logger
from redis_history import history
from schemas import DBType


def llm_chatting(
    question: str,
    db_type: DBType,
    sql_required: bool,
) -> tuple[str, str] | str:
    """
    Отправляет текстовый запрос в Ollama и возвращает ответ пользователю.

    Если параметр sql_required=True функция вернет SQL-запрос с объяснением,
    иначе будет возвращен простой ответ на вопрос.
    Сохраняет запрос пользователя и ответ llm в redis.
    """

    logger.debug("Запрос пользователя: %s", question)

    history.add_user_message(question)

    llm = Ollama(model=settings.llm.model, temperature=0.2)
    if not sql_required:
        general_prompt = build_general_prompt(question, db_type)
        general_chain = general_prompt | llm
        general_response = general_chain.invoke({})
        history.add_ai_message(general_response)

        logger.debug("Ответ LLM: %s", general_response)

        return general_response
    else:
        sql_prompt = build_sql_prompt(question, db_type)
        sql_chain = sql_prompt | llm
        sql_response = sql_chain.invoke({})
        history.add_ai_message(sql_response)

        logger.debug("Ответ LLM c sql-запросом: %s", sql_response)

        try:
            sql_query, explanation = sql_response.split("|||")
        except ValueError:
            logger.warning("Ответ LLM не содержит разделителей |||: %s", sql_response)
            return sql_response
        return sql_query, explanation


def build_sql_prompt(question: str, db_type: DBType):
    """Создает messages с историей сообщений, настраивает промпты и отдает полученный messages."""

    if db_type == DBType.sqlite:
        system_prompt = get_sqlite_prompt()
    elif db_type == DBType.vertica:
        system_prompt = get_vertica_prompt()
    else:
        raise ValueError(f"Неподдерживаемый тип БД: {db_type}")

    return ChatPromptTemplate.from_messages(
        [("system", system_prompt), *history.messages, ("human", question)]
    )


def build_general_prompt(question: str, db_type: DBType):
    system_prompt = get_general_vertica_prompt(db_type)

    return ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("human", question)]
    )
