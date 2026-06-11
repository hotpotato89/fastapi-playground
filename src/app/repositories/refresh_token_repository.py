from datetime import datetime
import logging

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.exceptions import DatabaseError
from src.app.models import RefreshToken


logger = logging.getLogger(__name__)
ERROR_FIELD: str = "Database error, we are working about it"


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _commit_or_error(self, object: RefreshToken) -> RefreshToken:
        self.session.add(object)
        try:
            await self.session.commit()
            await self.session.refresh(object)
            return object
        except Exception as e:
            logger.error("Database Error", exc_info=e)
            raise DatabaseError(ERROR_FIELD)

    async def _commit_deletion_or_error(self) -> None:
        try:
            await self.session.commit()
        except Exception as e:
            logger.error("Database Error", exc_info=e)
            raise DatabaseError(ERROR_FIELD)

    async def create(
        self, token: str, user_id: int, expires_at: datetime
    ) -> RefreshToken:
        new_token = RefreshToken(user_id=user_id, token=token, expires_at=expires_at)
        return await self._commit_or_error(new_token)

    async def get_by_token(self, token: str) -> RefreshToken | None:
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token == token)
        )
        return result.scalar_one_or_none()

    async def revoke_by_token(self, token: str) -> None:
        await self.session.execute(
            delete(RefreshToken).where(RefreshToken.token == token)
        )
        await self._commit_deletion_or_error()

    async def revoke_all_by_user_id(self, user_id: int) -> None:
        await self.session.execute(
            delete(RefreshToken).where(RefreshToken.user_id == user_id)
        )
        await self._commit_deletion_or_error()
