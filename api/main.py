import uvicorn
from fastapi import FastAPI

from llm_client import generate_sql
from responses import ask_responses
from schemas import UserRequest, AssistentResponse
from sql_runner import execute_sql_query

app = FastAPI()


@app.post("/ask", responses=ask_responses)
def ask_bot(user_request: UserRequest) -> AssistentResponse:
    sql_query = generate_sql(user_request.question)
    result = execute_sql_query(sql_query)
    return {"sql_query": sql_query, "result": result}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
