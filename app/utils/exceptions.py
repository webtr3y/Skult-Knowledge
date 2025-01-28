"""
Custom Exception Classes

Centralizes all custom exceptions and their handling.
"""

from typing import Any, Dict, Optional
from fastapi import HTTPException
from loguru import logger

class AppException(HTTPException):
    """Base exception for application errors"""
    def __init__(
        self,
        status_code: int = 500,
        detail: str = "Internal server error",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        logger.error(f"AppException: {detail}")

class ValidationError(AppException):
    """Raised when input validation fails"""
    def __init__(self, detail: str = "Validation error"):
        super().__init__(status_code=400, detail=detail)

class RateLimitError(AppException):
    """Raised when rate limit is exceeded"""
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(status_code=429, detail=detail)

class AuthenticationError(AppException):
    """Raised when authentication fails"""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(status_code=401, detail=detail)

class ResourceNotFoundError(AppException):
    """Raised when a requested resource is not found"""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail) 