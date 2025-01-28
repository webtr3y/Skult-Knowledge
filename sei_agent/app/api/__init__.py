"""
API Routes Package

Initializes all API routes.
"""

from fastapi import APIRouter
from .routes import router as api_router

# Create main API router
api_router = APIRouter()

# Include all route modules
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])

# Initialize API components

__all__ = ['api_router'] 