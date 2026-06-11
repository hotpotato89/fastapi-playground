from datetime import datetime, timezone
from typing import Any

from src.app.exceptions import InvalidCredentialsError
from src.app.models import User
from src.app.repositories.refresh_token_repository import RefreshTokenRepository
from src.app.repositories.user_repository import UserRepository
from src.app.schemas.user_schemas import UserLogin, UserRegister, UserResponse
from src.app.utils.hash import hash_password, verify_password
from src.app.utils.jwt import create_access_token, create_refresh_token, decode_jwt


class UserService:
    def __init__(
        self, repo: UserRepository, refresh_token_repo: RefreshTokenRepository
    ) -> None:
        self.repo = repo
        self.refresh_token_repo = refresh_token_repo

    async def register_user(self, userdata: UserRegister) -> UserResponse:
        return await self.repo.register(
            userdata.username, hash_password(userdata.password.get_secret_value())
        )

    async def login_user(self, userdata: UserLogin) -> dict[str, Any]:
        user = await self.repo.get_by_username_for_auth(userdata.username)
        if not user or not verify_password(
            userdata.password.get_secret_value(), user.password_hash
        ):
            raise InvalidCredentialsError("Invalid password or login")
        access_token = create_access_token(user.id, user.username)
        refresh_token = create_refresh_token(user.id, user.username)

        token_payload = decode_jwt(refresh_token)
        expires_at = datetime.fromtimestamp(token_payload["exp"], tz=timezone.utc)

        await self.refresh_token_repo.create(refresh_token, user.id, expires_at)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }

    async def get_me(self, user: User) -> UserResponse:
        return UserResponse.model_validate(user)
