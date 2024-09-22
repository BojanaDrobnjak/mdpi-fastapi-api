from typing import Optional

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from loguru import logger
from mdpi_api.services.auth_service import AuthService
from mdpi_api.services.jwt_service import JWTService
from mdpi_api.settings import Settings
from mdpi_api.web.api.errors.auth import JWTError
from mdpi_api.web.api.schemas.auth import DecodedTokenResponse

jwt_settings = Settings().jwt


class JWTBearer(HTTPBearer):
    """
    Custom class for handling JWT-based authentication.

    This class extends FastAPI's HTTPBearer and provides additional functionality
    for validating JWT tokens in the authorization header.

    :param auto_error: Whether to automatically raise
        an HTTPException on authentication failure.
    """

    def __init__(self, auto_error: bool = False):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self,
        request: Request,
        auth_service: AuthService = Depends(),
    ) -> Optional[HTTPAuthorizationCredentials]:
        """
        Perform the JWT token authentication.

        This method is called by FastAPI during the authentication process.
        It extends the functionality of FastAPI's HTTPBearer.

        :param request: The FastAPI Request object.
        :param auth_service: The AuthService object.
        :return: HTTPAuthorizationCredentials if the token is valid, None otherwise.

        :raises JWTError: If there are incorrect credentials values.
        """
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(
            request,
        )
        if credentials:
            jwt_decoded = await self.validate_credentials(credentials)
            await auth_service.authenticate_user(jwt_decoded, request)
            return credentials

        raise JWTError(detail="Invalid authorization code.")

    @staticmethod
    async def validate_credentials(
        credentials: HTTPAuthorizationCredentials,
    ) -> DecodedTokenResponse:
        """
        Validate the credentials.

        :param credentials: The HTTPAuthorizationCredentials object.
        :return: The decoded JWT token.

        :raises JWTError: If there are incorrect credentials values.
        """
        if credentials.scheme != "Bearer":
            raise JWTError(detail="Invalid authentication scheme.")

        jwt_service = JWTService()
        if not jwt_service.verify_jwt(credentials.credentials):
            raise JWTError(detail="Invalid token or expired token.")

        jwt_decoded = jwt_service.decode_jwt(credentials.credentials)
        logger.info(f"jwt_decoded: {jwt_decoded}")

        if jwt_decoded.token_type != jwt_settings.default_token_type:
            raise JWTError(detail="Invalid token type.")

        return jwt_decoded
