from src.app.repositories.user_repository import UserRepository
from src.app.schemas.user_schemas import UserRegister, UserResponse
from src.app.utils.hashing import hash_password


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register_user(self, userdata: UserRegister) -> UserResponse:
        return await self.repo.register(
            userdata.username, hash_password(userdata.password.get_secret_value())
        )
