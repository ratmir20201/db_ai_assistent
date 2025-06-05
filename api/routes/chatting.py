from fastapi import Depends, APIRouter, HTTPException, Request
from sqlalchemy.orm import Session

from auth.auth_routers import fastapi_users
from database.db import get_session
from models.user import User
from responses import ask_responses
from schemas import UserRequest, AssistentResponse
from services import get_sql_query_explanation_result_message_id

router = APIRouter(prefix="/chat", tags=["Chatting"])


@router.post("/messages", responses=ask_responses)
def ask_bot(
    user_request: UserRequest,
    request: Request,
    session: Session = Depends(get_session),
    current_user: User = Depends(fastapi_users.current_user()),
) -> AssistentResponse:
    response = get_sql_query_explanation_result_message_id(
        user_request,
        request,
        session,
    )

    return AssistentResponse(**response)
