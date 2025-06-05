from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse


async def unauth_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401 and request.headers.get("accept", "").startswith(
        "text/html"
    ):
        return RedirectResponse("/login")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
