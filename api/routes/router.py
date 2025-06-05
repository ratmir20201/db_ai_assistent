from fastapi import APIRouter

from routes.chatting import router as chat_router
from routes.message_feedback import router as message_review_router

main_router = APIRouter(prefix="/api")

main_router.include_router(chat_router)
main_router.include_router(message_review_router)
