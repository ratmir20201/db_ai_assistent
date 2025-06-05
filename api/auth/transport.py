from fastapi_users.authentication import BearerTransport, CookieTransport

bearer_transport = BearerTransport(tokenUrl="auth/login")

cookie_transport = CookieTransport(
    cookie_name="accessToken",
    cookie_max_age=3600,
    cookie_samesite="lax",
)
