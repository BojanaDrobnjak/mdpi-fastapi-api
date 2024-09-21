from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import UJSONResponse
from fastapi.staticfiles import StaticFiles
from mdpi_api.logging import configure_logging
from mdpi_api.settings import Settings
from mdpi_api.web.api.exception_handlers import (
    HTTPExceptionResponseModelError,
    http_exception_handler,
    request_validation_exception_handler,
)
from mdpi_api.web.api.router import api_router
from mdpi_api.web.lifetime import register_shutdown_event, register_startup_event
from mdpi_api.web.middlewares.rate_limiter import RateLimiterMiddleware
from mdpi_api.web.utils.token_bucket import TokenBucket
from starlette.middleware.sessions import SessionMiddleware

APP_ROOT = Path(__file__).parent.parent
settings = Settings()


def add_exception_handlers(api: FastAPI) -> None:
    """
    Add exception handlers to the provided FastAPI instance.

    :param api: FastAPI instance.
    """
    api.add_exception_handler(
        RequestValidationError,
        request_validation_exception_handler,
    )
    api.add_exception_handler(
        HTTPExceptionResponseModelError,
        http_exception_handler,
    )


def add_middlewares(app: FastAPI) -> None:
    """
    Add middlewares to the provided FastAPI instance.

    :param app: FastAPI instance.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.security.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.security.allowed_hosts,
    )
    # Authlib will use request.session to store temporary codes and states
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.security.session_secret_key,
    )
    app.add_middleware(
        RateLimiterMiddleware,
        bucket=TokenBucket(
            capacity=settings.rate_limit.capacity,
            refill_rate=settings.rate_limit.refill_rate,
        ),
    )
    # TODO: add request context log middleware


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="mdpi_api",
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Adds exception handlers.
    add_exception_handlers(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )

    return app
