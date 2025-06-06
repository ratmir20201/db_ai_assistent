from fastapi import APIRouter, Depends
from starlette.responses import FileResponse

from auth.auth_routers import fastapi_users
from config import STATIC_DIR
from models.user import User

router = APIRouter(tags=["Templates"])


@router.get("/")
async def main_page(user: User = Depends(fastapi_users.current_user())):
    response = FileResponse(STATIC_DIR / "index.html")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@router.get("/login")
async def login_page():
    response = FileResponse(STATIC_DIR / "login.html")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@router.get("/admin")
async def admin_page(user: User = Depends(fastapi_users.current_user(superuser=True))):
    return FileResponse(STATIC_DIR / "admin.html")
