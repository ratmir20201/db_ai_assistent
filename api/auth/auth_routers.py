from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers

from auth.backend import auth_backend
from auth.user_manager import get_user_manager
from models.user import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(auth_backend),
)


@router.get("/current-user")
def get_current_user(user: User = Depends(fastapi_users.current_user())):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user
