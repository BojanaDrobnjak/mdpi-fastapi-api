from fastapi.params import Depends
from fastapi.routing import APIRouter
from mdpi_api.web.api import auth, cities, docs, favorites
from mdpi_api.web.middlewares.jwt_bearer import JWTBearer

api_router = APIRouter()
api_router.include_router(docs.router)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(
    cities.router,
    prefix="/cities",
    tags=["cities"],
    dependencies=[Depends(JWTBearer())],
)
api_router.include_router(
    favorites.router,
    prefix="/favorites",
    tags=["favorites"],
    dependencies=[Depends(JWTBearer())],
)
