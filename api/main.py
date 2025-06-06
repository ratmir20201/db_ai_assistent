import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from action.user_creation import create_superuser
from auth.auth_routers import router as auth_router
from config import settings, STATIC_DIR
from exception_handlers.unauth_handler import unauth_exception_handler
from routes.router import main_router
from routes.templates import router as template_router


async def lifespan(app: FastAPI):
    await create_superuser(
        email=settings.api.superuser_email,
        username=settings.api.superuser_name,
        password=settings.api.superuser_password,
    )
    yield


app = FastAPI(lifespan=lifespan)


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


app.include_router(main_router)
app.include_router(auth_router)
app.include_router(template_router)

app.add_exception_handler(HTTPException, unauth_exception_handler)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
