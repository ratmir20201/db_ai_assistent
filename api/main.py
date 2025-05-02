from pathlib import Path

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from llm_clients.mistral.mistral_client import generate_sql
from redis_client import redis_client
from responses import ask_responses
from schemas import AssistentResponse, UserRequest
from sql_executors.executor import execute_sql


async def lifespan(app: FastAPI):
    redis_client.flushdb()
    yield


app = FastAPI(lifespan=lifespan)

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "frontend"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ask", responses=ask_responses)
def ask_bot(user_request: UserRequest) -> AssistentResponse:
    sql_response = generate_sql(user_request.question, user_request.db_type)
    sql_query, explanation = sql_response.split("|||")

    sql_query = sql_query.strip()
    explanation = explanation.strip()

    result = execute_sql(sql_query, user_request.db_type)
    return AssistentResponse(
        sql_query=sql_query,
        result=result,
        explanation=explanation,
    )


@app.get("/")
def main_title():
    return FileResponse(STATIC_DIR / "index.html")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
