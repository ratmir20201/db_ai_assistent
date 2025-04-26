import uvicorn
from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from llm_client import generate_sql
from schemas import UserRequest

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_index():
    return FileResponse("static/index.html")


@app.post("/ask")
def ask_bot(user_request: UserRequest):
    sql_query = generate_sql(user_request.question)
    return {"sql_query": sql_query}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
