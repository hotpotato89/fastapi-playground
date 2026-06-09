from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.app.exceptions import UserAlreadyExistsError, UserNotFoundError
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
            raise UserAlreadyExistsError(
                f"User with username: {username} already exists"
            )

    async def get_by_id_for_auth(self, id: int) -> User:
        result = await self.session.execute(select(User).where(User.id == id))
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotFoundError(f"User with ID {id} does not exist")
        return user

    async def get_by_username_for_auth(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
