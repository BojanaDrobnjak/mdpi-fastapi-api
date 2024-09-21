import enum
from contextvars import ContextVar

from mdpi_api.settings import settings
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

CURRENT_LOCALE_CTX_KEY = "current_locale"

_current_locale_ctx_var: ContextVar[str] = ContextVar(
    CURRENT_LOCALE_CTX_KEY,
    default=settings.default_locale,
)


def get_locale() -> str:
    """
    Get current locale from context.

    :return: current locale.
    """
    return _current_locale_ctx_var.get()


class LocaleEnum(enum.Enum):
    """Enum for locale."""

    EN = "en"
    SR = "sr"


class I18nMiddleware(BaseHTTPMiddleware):
    """Middleware to add locale to request context."""

    WHITE_LIST = {locale.value for locale in LocaleEnum}
    DEFAULT_LOCALE = settings.default_locale

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """
        Dispatch request and add locale to request context.

        :param request: request to dispatch.
        :param call_next: next middleware to call.
        :return: response.
        """
        locale = (
            request.headers.get("Accept-Language", None)
            or request.path_params.get("locale", None)
            or request.query_params.get("locale", None)
            or self.DEFAULT_LOCALE
        )

        if locale not in self.WHITE_LIST:
            locale = self.DEFAULT_LOCALE
        request.state.locale = locale
        _current_locale_ctx_var.set(locale)

        return await call_next(request)
