import enum
import time
import uuid
from typing import Dict

import jwt
from fastapi import status
from loguru import logger
from mdpi_api.settings import Settings
from mdpi_api.web.api.errors.auth import JWTError
from mdpi_api.web.api.schemas.auth import DecodedTokenResponse
from pydantic import UUID4

jwt_settings = Settings().jwt


class JWTTokenTypeEnum(enum.Enum):
    """Enumeration for JWT token types."""

    ACCESS = "access"
    REFRESH = "refresh"


class JWTService:
    """Class for jwt service."""

    @staticmethod
    def sign_jwt(
        user_id: UUID4,
        token_type: JWTTokenTypeEnum = JWTTokenTypeEnum.ACCESS,
    ) -> str:
        """
        Sign a JWT token for the specified user.

        :param user_id: ID of the user.
        :param token_type: The type of the token.
        :return: A string containing the signed JWT token.
        """
        expiry_time = (
            jwt_settings.expiry_time
            if token_type == JWTTokenTypeEnum.ACCESS
            else jwt_settings.refresh_expiry_time
        )
        jti = str(uuid.uuid4())
        return jwt.encode(
            {
                "sub": str(user_id),
                "expires": time.time() + expiry_time,
                "token_type": token_type.value,
                "jti": jti,
            },
            jwt_settings.secret,
            algorithm=jwt_settings.algorithm,
        )

    @staticmethod
    def validate_jwt_structure(token: str) -> None:
        """
        Validate the structure of the JWT token.

        :param token: The JWT token to be validated.
        :raises ValueError: If the JWT structure is invalid.
        """
        segments = token.split(".")
        if len(segments) != 3:
            raise ValueError("Invalid JWT structure")

    @staticmethod
    def get_error_code(refresh: bool = False) -> int:
        """
        Get the error code for the JWT error.

        :param refresh: Whether the token is a refresh token.
        :return: The error code.
        """
        return status.HTTP_401_UNAUTHORIZED if refresh else status.HTTP_403_FORBIDDEN

    def validate_token_expiration(
        self,
        decoded_token: Dict[str, float],
        refresh: bool = False,
    ) -> None:
        """
        Validate the expiration of the decoded JWT token.

        :param decoded_token: The decoded JWT token to be validated.
        :param refresh: Whether the token is a refresh token.
        :raises JWTError: If the JWT token has expired.
        """
        if decoded_token["expires"] < time.time():
            error_code = self.get_error_code(refresh)
            logger.warning(f"JWT expired [refresh: {refresh}]")
            raise JWTError(detail="JWT expired", status_code=error_code)

    def verify_jwt(self, jwt_token: str) -> bool:
        """
        Verify the validity of a JWT token.

        :param jwt_token: The JWT token to be verified.
        :return: True if the token is valid, False otherwise.
        """
        is_token_valid: bool = False

        try:
            payload = self.decode_jwt(jwt_token)
        except Exception as exception:
            logger.warning(f"JWT decoding error: {exception}")
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid

    def decode_jwt(self, token: str, refresh: bool = False) -> DecodedTokenResponse:
        """
        Decode a JWT token and validate its structure and expiration.

        :param token: The JWT token to be decoded.
        :param refresh: Whether the token is a refresh token.
        :return: Decoded payload if the token is valid, None otherwise.

        :raises JWTError: If the JWT token has expired or is invalid.
        :raises Exception: If an error occurs during decoding.
        """
        error_code = self.get_error_code(refresh)
        try:
            self.validate_jwt_structure(token)
            decoded_token = jwt.decode(
                token,
                jwt_settings.secret,
                algorithms=[jwt_settings.algorithm],
            )
            self.validate_token_expiration(decoded_token, refresh)
            return DecodedTokenResponse(**decoded_token)
        except jwt.ExpiredSignatureError:
            logger.warning("JWT expired")
            raise JWTError(detail="JWT expired", status_code=error_code)
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT")
            raise JWTError(detail="Invalid JWT", status_code=error_code)
        except Exception as exception:
            logger.error(f"JWT decoding error: {exception}")
            raise exception
