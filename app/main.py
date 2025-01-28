"""
Application Entry Point

Handles application creation and configuration.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import uvicorn
from typing import Optional
import asyncio

from .config.settings import settings
from .utils.logging import setup_logging
from .utils.resource_manager import ResourceManager
from .middleware.security import SecurityMiddleware
from .middleware.rate_limiter import RateLimitMiddleware
from .routes import api_router
from .utils.exceptions import AppException

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    # Initialize logging
    setup_logging()
    
    # Create FastAPI app
    app = FastAPI(
        title="SEI Agent",
        description="AI-powered SEI Network analytics and engagement platform",
        version="1.0.0",
        docs_url=None if settings.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if settings.ENVIRONMENT == "production" else "/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add security middleware
    app.add_middleware(SecurityMiddleware)
    
    # Add rate limiting
    app.add_middleware(RateLimitMiddleware)
    
    # Exception handlers
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
    
    # Health check
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    # Include routers
    app.include_router(api_router, prefix="/api")
    
    # Startup and shutdown events
    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting application")
        app.state.resource_manager = ResourceManager()
        await app.state.resource_manager.initialize()
        
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down application")
        if hasattr(app.state, "resource_manager"):
            await app.state.resource_manager.cleanup()
    
    return app

def run_app():
    """Run the application"""
    app = create_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

if __name__ == "__main__":
    run_app() 