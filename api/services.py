from typing import Any

from fastapi import Request
from sqlalchemy.orm import Session

from crud.messages import create_bot_message
from llms.base_llm import BaseLLM
from llms.llms import get_llm_by_type
from redis_history import get_history
from schemas import UserRequest


def get_sql_query_explanation_result_message_id(
    user_request: UserRequest,
    request: Request,
    session: Session,
) -> dict[str, Any]:
    """
    Возвращает sql-запрос сгенерированный llm, объяснение и результат его выполнения.

    Либо если sql-запрос не нужен возвращает ответ на вопрос пользователя.
    """

    session_id = request.headers.get("X-Session-ID")
    LLMClass = get_llm_by_type(user_request.llm_type)
    history = get_history(session_id)

    llm: BaseLLM = LLMClass(
        question=user_request.question,
        db_type=user_request.db_type.lower(),
        sql_required=user_request.sql_required,
        history=history,
    )
    llm_response = llm.get_llm_response()

    message_id = create_bot_message(session, llm_response)

    if isinstance(llm_response, tuple):
        sql_query, explanation = llm_response
        sql_query = sql_query.strip()
        explanation = explanation.strip()
        # sql_script_result = execute_sql(sql_query, user_request.db_type.lower())
        sql_script_result = ""
        return {
            "sql_query": sql_query,
            "explanation": explanation,
            "sql_script_result": sql_script_result,
            "message_id": message_id,
        }

    return {
        "sql_query": "",
        "explanation": llm_response,
        "sql_script_result": "",
        "message_id": message_id,
    }
