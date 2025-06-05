from fastapi_users.authentication import AuthenticationBackend

from auth.strategy import get_database_strategy
from auth.transport import cookie_transport

auth_backend = AuthenticationBackend(
    name="access-tokens-db",
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)
