from typing import Any
from datetime import datetime, timezone, timedelta
import jwt

from src.app.core import settings
from src.app.exceptions import InvalidTokenError


def encode_jwt(
    data: dict[str, Any], expire_minute: int = 15, token_type: str = "access"
) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expire_minute)
    to_encode.update({"exp": expire, "iat": now, "type": token_type})
    return jwt.encode(to_encode, settings.jwt.secret_key, settings.jwt.algorithm)


def decode_jwt(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.jwt.secret_key, [settings.jwt.algorithm])
    except jwt.exceptions.DecodeError:
        raise InvalidTokenError("Invalid token")
    except jwt.exceptions.ExpiredSignatureError:
        raise InvalidTokenError("Token has expired")
