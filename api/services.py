from llm_clients.mistral.mistral_client import generate_sql
from schemas import UserRequest
from sql_executors.executor import execute_sql


def get_sql_query_explanation_result(user_request: UserRequest):
    sql_query, explanation = generate_sql(
        user_request.question,
        user_request.db_type.lower(),
    )

    if not explanation:
        return "", sql_query, ""

    sql_query = sql_query.strip()
    explanation = explanation.strip()

    # result = execute_sql(sql_query, user_request.db_type.lower())
    result = ""

    return sql_query, explanation, result
