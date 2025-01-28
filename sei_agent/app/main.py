from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import uvicorn
from typing import Dict, List

from .config.settings import Settings
from .utils.logging import setup_logging
from .utils.resource_manager import ResourceManager
from .middleware.security import SecurityMiddleware
from .middleware.rate_limiter import RateLimitMiddleware
from .api.routes import router as api_router
from .utils.exceptions import AppException
from .services import BlockchainService, TwitterService

settings = Settings()

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    setup_logging()
    
    app = FastAPI(
        title="SEI Network Analytics Agent",
        description="Analytics and social media automation for SEI Network",
        version="1.0.0"
    )

    # Configure middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(SecurityMiddleware)
    app.add_middleware(RateLimitMiddleware)

    # Register exception handlers
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(f"Global exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check() -> Dict[str, str]:
        """Health check endpoint."""
        try:
            return {"status": "healthy"}
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Service unhealthy")

    # Include API routes
    app.include_router(api_router, prefix="/api")

    # Startup and shutdown events
    @app.on_event("startup")
    async def startup_event() -> None:
        """Initialize services on startup."""
        logger.info("Starting application")
        try:
            # Initialize services
            app.state.resource_manager = ResourceManager()
            await app.state.resource_manager.initialize()
            
            app.state.blockchain = BlockchainService()
            if not await app.state.blockchain.verify_connection():
                raise AppException(status_code=500, detail="Blockchain connection failed")
            
            app.state.twitter = TwitterService()
            logger.info("Application started successfully")
        except Exception as e:
            logger.error(f"Failed to start application: {str(e)}")
            raise AppException(status_code=500, detail="Failed to initialize services")

    @app.on_event("shutdown")
    async def shutdown_event() -> None:
        """Cleanup on shutdown."""
        logger.info("Shutting down application")
        try:
            if hasattr(app.state, "resource_manager"):
                await app.state.resource_manager.cleanup()
            if hasattr(app.state, "blockchain"):
                await app.state.blockchain.close()
            logger.info("Application shutdown complete")
        except Exception as e:
            logger.error(f"Error during shutdown: {str(e)}")

    @app.get("/api/trending/topics")
    async def get_trending_topics() -> Dict[str, List[Dict]]:
        """Get trending topics endpoint."""
        try:
            # Example response matching frontend interface
            return {
                "trending_topics": [
                    {
                        "topic": "SEI",
                        "data": {
                            "mention_count": 150,
                            "avg_engagement": 45.5,
                            "mentions_per_hour": 12,
                            "sentiment_distribution": {
                                "positive": 0.6,
                                "neutral": 0.3,
                                "negative": 0.1
                            }
                        }
                    },
                    {
                        "topic": "DeFi",
                        "data": {
                            "mention_count": 120,
                            "avg_engagement": 38.2,
                            "mentions_per_hour": 10,
                            "sentiment_distribution": {
                                "positive": 0.5,
                                "neutral": 0.4,
                                "negative": 0.1
                            }
                        }
                    }
                ]
            }
        except Exception as e:
            logger.error(f"Error getting trending topics: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to get trending topics")

    return app

def run_server() -> None:
    """Run the application server."""
    try:
        logger.info("Starting server...")
        app = create_app()
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Server failed to start: {str(e)}")
        raise

if __name__ == "__main__":
    run_server() 