from fastapi import APIRouter
from mdpi_api.settings import Settings

router = APIRouter()

jwt_settings = Settings().jwt
