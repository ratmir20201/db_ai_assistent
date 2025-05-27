from fastapi import FastAPI, Depends, APIRouter
from fastapi import Request
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from database.db import get_session
from responses import ask_responses
from schemas import UserRequest, AssistentResponse
from services import get_sql_query_explanation_result

router = APIRouter(prefix="/chat", tags=["chatting"])


@router.post("/ask", responses=ask_responses)
def ask_bot(
    user_request: UserRequest,
    request: Request,
    session: Session = Depends(get_session),
) -> AssistentResponse:
    response = get_sql_query_explanation_result(user_request, request, session)

    if isinstance(response, tuple):
        sql_query, explanation, sql_script_result = response

        return AssistentResponse(
            sql_query=sql_query,
            sql_script_result=sql_script_result,
            explanation=explanation,
        )

    return AssistentResponse(sql_query="", sql_script_result="", explanation=response)
