from llm_clients.mistral.mistral_client import llm_chatting
from schemas import UserRequest


def get_sql_query_explanation_result(user_request: UserRequest) -> tuple | str:
    llm_response = llm_chatting(
        question=user_request.question,
        db_type=user_request.db_type.lower(),
    )

    if isinstance(llm_response, tuple):
        sql_query, explanation = llm_response
        sql_query = sql_query.strip()
        explanation = explanation.strip()
        # result = execute_sql(sql_query, user_request.db_type.lower())
        result = ""
        return sql_query, explanation, result

    return llm_response
