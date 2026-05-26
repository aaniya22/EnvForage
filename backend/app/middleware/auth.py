"""
Global API key authentication middleware.

Implements a deny-by-default security perimeter for all sensitive API routes.
Public routes (health check, docs, openapi schema) are explicitly exempted.

Configuration:
    Set the ``API_KEY`` environment variable to enable authentication.
    If ``API_KEY`` is not set, the middleware is disabled (development mode).

Usage:
    The middleware is registered globally in ``app/main.py`` and applies
    to all requests automatically. No per-route decoration is needed.

    Clients must send the API key in one of:
        - ``Authorization: Bearer <api_key>`` header
        - ``X-API-Key: <api_key>`` header
"""
import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import get_settings

logger = logging.getLogger(__name__)

# Routes that do not require authentication
PUBLIC_ROUTES: set[str] = {
    "/health",
    "/api/docs",
    "/api/redoc",
    "/api/openapi.json",
}


class APIKeyMiddleware(BaseHTTPMiddleware):
    """
    Deny-by-default middleware that requires a valid API key for
    all routes except those listed in PUBLIC_ROUTES.

    If ``settings.api_key`` is None or empty, the middleware is
    disabled and all requests pass through (development mode).
    """

    async def dispatch(self, request: Request, call_next):
        settings = get_settings()

        # Middleware disabled if no API key is configured
        if not settings.api_key:
            return await call_next(request)

        # Allow public routes without authentication
        if request.url.path in PUBLIC_ROUTES:
            return await call_next(request)

        # Extract API key from headers
        api_key = self._extract_api_key(request)

        if api_key != settings.api_key:
            logger.warning(
                "Unauthorized request to %s from %s",
                request.url.path,
                request.client.host if request.client else "unknown",
            )
            return JSONResponse(
                status_code=401,
                content={
                    "error": "UNAUTHORIZED",
                    "message": (
                        "Missing or invalid API key. "
                        "Provide a valid key via 'Authorization: Bearer <key>' "
                        "or 'X-API-Key: <key>' header."
                    ),
                },
            )

        return await call_next(request)

    def _extract_api_key(self, request: Request) -> str | None:
        """Extract API key from Authorization or X-API-Key header."""
        # Check Authorization: Bearer <token>
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            return auth_header[len("Bearer "):]

        # Check X-API-Key header
        return request.headers.get("X-API-Key")
