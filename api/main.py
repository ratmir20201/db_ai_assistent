import uvicorn
from fastapi import FastAPI

from llm_client import generate_sql
from schemas import UserRequest
from sql_runner import execute_sql

app = FastAPI()


@app.post("/ask")
def ask_bot(user_request: UserRequest):
    sql_query = generate_sql(user_request.question)
    result = execute_sql(sql_query)
    return {"sql_query": sql_query, "result": result}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
