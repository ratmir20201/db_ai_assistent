from llms.base_llm import BaseLLM
from llms.llms import get_llm_by_type
from schemas import UserRequest


def get_sql_query_explanation_result(user_request: UserRequest) -> tuple | str:
    """
    Возвращает sql-запрос сгенерированный llm, объяснение и результат его выполнения.

    Либо если sql-запрос не нужен возвращает ответ на вопрос пользователя.
    """

    LLMClass = get_llm_by_type(user_request.llm_type)
    llm: BaseLLM = LLMClass(
        question=user_request.question,
        db_type=user_request.db_type.lower(),
        sql_required=user_request.sql_required,
    )
    llm_response = llm.llm_chatting()

    if isinstance(llm_response, tuple):
        sql_query, explanation = llm_response
        sql_query = sql_query.strip()
        explanation = explanation.strip()
        # sql_script_result = execute_sql(sql_query, user_request.db_type.lower())
        sql_script_result = ""
        return sql_query, explanation, sql_script_result

    return llm_response
