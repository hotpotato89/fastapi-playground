from src.app.exceptions import InvalidCredentialsError
from src.app.models import User
from src.app.repositories.user_repository import UserRepository
from src.app.schemas.user_schemas import UserLogin, UserRegister, UserResponse
from src.app.utils.hash import hash_password, verify_password
from src.app.utils.jwt import create_access_token


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register_user(self, userdata: UserRegister) -> UserResponse:
        return await self.repo.register(
            userdata.username, hash_password(userdata.password.get_secret_value())
        )

    async def login_user(self, userdata: UserLogin) -> str:
        user = await self.repo.get_by_username_for_auth(userdata.username)
        if not user or not verify_password(
            userdata.password.get_secret_value(), user.password_hash
        ):
            raise InvalidCredentialsError("Invalid password or login")
        return create_access_token(user.id, user.username)

    async def get_me(self, user: User) -> UserResponse:
        return UserResponse.model_validate(user)
