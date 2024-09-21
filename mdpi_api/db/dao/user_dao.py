from typing import Optional

from fastapi import Depends
from loguru import logger
from mdpi_api.db.dependencies import get_db_session
from mdpi_api.db.models.user_model import UserModel
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class UserDAO:
    """Class for authenticating users."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        """
        Verify user credentials.

        :param email: email of the user.
        :return: True if credentials are verified, False otherwise.

        :raises Exception: If there is an error during the verification process.
        """
        try:
            result = await self.session.execute(
                select(UserModel).where(and_(UserModel.email == email)),
            )
            user = result.scalar()
            logger.info(f"User: {result}")
            return user
        except Exception as exception:
            logger.error(f"Failed to verify credentials: {exception}")
            raise exception
