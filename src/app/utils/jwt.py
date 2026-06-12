from typing import Any
from datetime import datetime, timezone, timedelta
import jwt

from src.app.core import settings
from src.app.exceptions import InvalidTokenError


def create_access_token(user_id: int, username: str) -> str:
    payload = {"sub": username, "user_id": user_id}
    return _encode_jwt(payload)


def create_refresh_token(user_id: int, username: str) -> str:
    payload = {"sub": username, "user_id": user_id}
    return _encode_jwt(payload, 60 * 24 * 7, "refresh")


def _encode_jwt(
    data: dict[str, Any], expire_minute: int = 15, token_type: str = "access"
) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expire_minute)
    to_encode.update({"exp": expire, "iat": now, "type": token_type})
    return jwt.encode(
        to_encode, settings.jwt.private_key_path.read_text(), settings.jwt.algorithm
    )


def decode_jwt(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            settings.jwt.public_key_path.read_text(),
            [settings.jwt.algorithm],
            options={"verify_signature": True},
        )
    except jwt.exceptions.DecodeError:
        raise InvalidTokenError("Invalid token")
    except jwt.exceptions.ExpiredSignatureError:
        raise InvalidTokenError("Token has expired")
