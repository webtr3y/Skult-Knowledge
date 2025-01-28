"""
Logging Configuration

Provides structured logging with proper formatting and handlers.
"""

import sys
from loguru import logger
from pathlib import Path
from ..config.settings import settings

def setup_logging():
    """Configure application logging"""
    
    # Remove default logger
    logger.remove()
    
    # Log format
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # Console handler
    logger.add(
        sys.stdout,
        format=log_format,
        level="DEBUG" if settings.DEBUG else "INFO",
        backtrace=True,
        diagnose=True
    )
    
    # File handler
    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)
    
    logger.add(
        log_path / "app.log",
        rotation="500 MB",
        retention="10 days",
        format=log_format,
        level="INFO",
        backtrace=True,
        diagnose=True
    )
    
    # Error file handler
    logger.add(
        log_path / "error.log",
        rotation="100 MB",
        retention="30 days",
        format=log_format,
        level="ERROR",
        backtrace=True,
        diagnose=True
    )

    return logger 