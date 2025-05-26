from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi import Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from responses import ask_responses
from schemas import AssistentResponse, UserRequest
from services import get_sql_query_explanation_result

app = FastAPI()

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
def ask_bot(user_request: UserRequest, request: Request) -> AssistentResponse:
    response = get_sql_query_explanation_result(user_request, request)

    if isinstance(response, tuple):
        sql_query, explanation, sql_script_result = response

        return AssistentResponse(
            sql_query=sql_query,
            sql_script_result=sql_script_result,
            explanation=explanation,
        )

    return AssistentResponse(sql_query="", sql_script_result="", explanation=response)


@app.get("/")
def main_title():
    return FileResponse(STATIC_DIR / "index.html")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
