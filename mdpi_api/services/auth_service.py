from fastapi import Depends
from loguru import logger
from mdpi_api.db.dao.user_dao import UserDAO
from mdpi_api.db.dependencies import get_db_session
from mdpi_api.services.jwt_service import JWTService, JWTTokenTypeEnum
from mdpi_api.web.api.errors.auth import NotAuthorizedError
from mdpi_api.web.api.schemas.auth import TokenResponse
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    """Class for auth service."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def verify_credentials(self, email: str, password: str) -> TokenResponse:
        """
        Verify user credentials.

        :param email: email of the user.
        :param password: password to verify.
        :return: TokenResponse if credentials are verified.

        :raises NotAuthorizedError: If the credentials are invalid.
        :raises Exception: If there is an error during the verification process.
        """
        try:
            user_dao = UserDAO(self.session)
            user = await user_dao.get_by_email(email)

            if user and user.verify_password(password):
                return await self.create_tokens(user.id)
            raise NotAuthorizedError("Invalid credentials")
        except Exception as exception:
            logger.error(f"Failed to verify credentials: {exception}")
            raise exception

    @staticmethod
    async def create_tokens(user_id: UUID4) -> TokenResponse:
        """
        Helper function to create access and refresh tokens for a user.

        :param user_id: ID of the user.
        :return: Dictionary containing access and refresh tokens.

        :raises Exception: If there is an error during the token creation process.
        """
        try:
            jwt_service = JWTService()
            access_token = jwt_service.sign_jwt(
                user_id=user_id,
                token_type=JWTTokenTypeEnum.ACCESS,
            )
            refresh_token = jwt_service.sign_jwt(
                user_id=user_id,
                token_type=JWTTokenTypeEnum.REFRESH,
            )

            return TokenResponse(access_token=access_token, refresh_token=refresh_token)

        except Exception as exception:
            logger.error(f"Error creating and storing tokens: {exception}")
            raise exception
