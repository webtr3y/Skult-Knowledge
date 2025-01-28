"""
SEI Agent Application

This module initializes all components of the SEI Agent application.
"""

from .config.settings import settings
from .utils.logging import setup_logging
from .utils.exceptions import AppException
from .middleware.base import BaseMiddleware
from .middleware.security import SecurityMiddleware
from .services.twitter import TwitterService
from .services.blockchain import BlockchainService

__version__ = "1.0.0"

# Initialize logging
setup_logging()

# Export commonly used components
__all__ = [
    "settings",
    "AppException",
    "BaseMiddleware",
    "SecurityMiddleware",
    "TwitterService",
    "BlockchainService",
] 