from fastapi.params import Depends
from fastapi.routing import APIRouter
from mdpi_api.web.api import docs, dummy
from mdpi_api.web.middlewares.jwt_bearer import JWTBearer

api_router = APIRouter()
api_router.include_router(docs.router)
api_router.include_router(
    dummy.router,
    prefix="/dummy",
    tags=["dummy"],
    dependencies=[Depends(JWTBearer())],
)
