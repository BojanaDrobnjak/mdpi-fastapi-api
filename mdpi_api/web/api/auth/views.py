from fastapi import APIRouter, Depends, Query
from loguru import logger
from mdpi_api.services.auth_service import AuthService
from mdpi_api.settings import Settings
from mdpi_api.web.api.schemas.api_response import APIResponse
from mdpi_api.web.api.schemas.auth import TokenResponse
from pydantic import EmailStr

router = APIRouter()

jwt_settings = Settings().jwt


@router.get("/token", response_model=APIResponse[TokenResponse])
async def get_token(
    email: EmailStr = Query(..., description="Email of the user"),
    password: str = Query(..., description="Password of the user"),
    auth_service: AuthService = Depends(),
) -> APIResponse[TokenResponse]:
    """
    This endpoint is used to get a token for a user with the given email and password.

    :param email: Email of the user.
    :param password: Password of the user.
    :param auth_service: AuthService dependency.
    :return: APIResponse containing the token.
    """
    logger.info(f"Getting token for user with email: {email}")
    result = await auth_service.verify_credentials(email, password)
    return APIResponse.create(
        message="auth-success",
        data=result,
    )
