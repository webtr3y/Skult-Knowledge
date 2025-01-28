"""
Base Middleware Configuration

Provides base classes and utilities for middleware components.
"""

from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable
from ..utils.exceptions import AppException
from loguru import logger

class BaseMiddleware(BaseHTTPMiddleware):
    """Base class for all middleware"""
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """Template method for middleware processing"""
        try:
            await self.before_request(request)
            response = await call_next(request)
            await self.after_request(response)
            return response
        except Exception as e:
            return await self.handle_error(e)

    async def before_request(self, request: Request) -> None:
        """Hook for processing before the request"""
        pass

    async def after_request(self, response: Response) -> None:
        """Hook for processing after the request"""
        pass

    async def handle_error(self, error: Exception) -> Response:
        """Handle middleware-specific errors"""
        if isinstance(error, AppException):
            return Response(
                content=error.detail,
                status_code=error.status_code,
                media_type="text/plain"
            )
        logger.error(f"Middleware error: {error}")
        return Response(
            content="Internal server error",
            status_code=500,
            media_type="text/plain"
        ) 