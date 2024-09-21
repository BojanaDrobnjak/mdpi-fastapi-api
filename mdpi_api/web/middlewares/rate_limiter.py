from fastapi import FastAPI, Request, Response, status
from loguru import logger
from mdpi_api.web.utils.token_bucket import TokenBucket
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """Rate limiter middleware."""

    def __init__(self, app: FastAPI, bucket: TokenBucket):
        super().__init__(app)
        self.bucket: TokenBucket = bucket

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """
        Dispatch incoming requests.

        :param request: Incoming request.
        :param call_next: Next middleware in the chain.
        :return: Response to the incoming request.
        """
        # Check if the request path starts with '/static'
        if request.url.path.startswith("/static"):
            # If it does, bypass the rate limiting logic
            return await call_next(request)

        # Process each incoming request
        if self.bucket.take_token():
            # If a token is available, proceed with the request
            return await call_next(request)
        # If no tokens are available, return a 429 error (rate limit exceeded)
        retry_after: float = self.bucket.capacity / self.bucket.refill_rate
        detail: str = f"Try again in {retry_after} sec."
        logger.warning(detail)
        return JSONResponse(
            content={
                "error": "",
                "message": "Rate limit exceeded",
                "detail": detail,
            },
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        )
