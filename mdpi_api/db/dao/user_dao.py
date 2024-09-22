from typing import Optional

from fastapi import Depends
from loguru import logger
from mdpi_api.db.dependencies import get_db_session
from mdpi_api.db.models.user_model import UserModel
from pydantic.v1 import UUID4
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class UserDAO:
    """Class for accessing users table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        """
        Get user by email.

        :param email: email of the user.
        :return: User object if found, None otherwise.

        :raises Exception: If there is an error during user retrieval.
        """
        try:
            result = await self.session.execute(
                select(UserModel).where(and_(UserModel.email == email)),
            )
            user = result.scalar()
            logger.info(f"User: {result}")
            return user
        except Exception as exception:
            logger.error(f"Failed to retrieve user: {exception}")
            raise exception

    async def get_by_id(self, user_id: UUID4) -> Optional[UserModel]:
        """
        Get user by id.

        :param user_id: id of the user.
        :return: User object if found, None otherwise.

        :raises Exception: If there is an error during user retrieval.
        """
        try:
            result = await self.session.execute(
                select(UserModel).where(and_(UserModel.id == user_id)),
            )
            user = result.scalar()
            logger.info(f"User: {result}")
            return user
        except Exception as exception:
            logger.error(f"Failed to retrieve user: {exception}")
            raise exception
