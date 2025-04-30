import uvicorn
from fastapi import FastAPI

from llm_client import generate_sql
from responses import ask_responses
from schemas import AssistentResponse, UserRequest
from sql_runner import execute_sql_query

app = FastAPI()


@app.post("/ask", responses=ask_responses)
def ask_bot(user_request: UserRequest) -> AssistentResponse:
    sql_response = generate_sql(user_request.question)
    sql_query, explanation = sql_response.split("|||")

    sql_query = sql_query.strip()
    explanation = explanation.strip()

    result = execute_sql_query(sql_query)
    return AssistentResponse(
        sql_query=sql_query,
        result=result,
        explanation=explanation,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
