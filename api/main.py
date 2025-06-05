from pathlib import Path

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from admin.model_admin import UserAdmin
from admin.user_creation import create_superuser
from auth.auth_routers import router as auth_router, fastapi_users
from config import settings
from database.db import engine
from exception_handlers.unauth_handler import unauth_exception_handler
from models.user import User
from routes.router import main_router


async def lifespan(app: FastAPI):
    await create_superuser(
        email=settings.api.superuser_email,
        username=settings.api.superuser_name,
        password=settings.api.superuser_password,
    )
    yield


app = FastAPI(lifespan=lifespan)
admin = Admin(app, engine)
admin.add_view(UserAdmin)


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "frontend"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://192.168.99.140:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main_title(user: User = Depends(fastapi_users.current_user())):
    response = FileResponse(STATIC_DIR / "index.html")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.get("/login")
async def login_page():
    response = FileResponse(STATIC_DIR / "login.html")
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


app.include_router(main_router)
app.include_router(auth_router)

app.add_exception_handler(HTTPException, unauth_exception_handler)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
