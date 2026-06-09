from sqlalchemy.exc import IntegrityError

from src.app.exceptions import UserAlreadyExistsError
from src.app.schemas.user_schemas import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def register(self, username: str, password_hash: str) -> UserResponse:
        new_user = User(username=username, password_hash=password_hash)
        self.session.add(new_user)
        try:
            await self.session.commit()
            await self.session.refresh(new_user)
            return UserResponse.model_validate(new_user)
        except IntegrityError:
            await self.session.rollback()
            raise UserAlreadyExistsError(f"User with username: {username} already exists")
