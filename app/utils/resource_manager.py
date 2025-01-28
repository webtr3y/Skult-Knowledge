"""
Resource Manager

Handles initialization and cleanup of application resources.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
import aiohttp
import redis.asyncio as redis
from loguru import logger
from ..config.settings import settings

class ResourceManager:
    def __init__(self):
        self.http_session: Optional[aiohttp.ClientSession] = None
        self.redis_client: Optional[redis.Redis] = None
        
    async def initialize(self):
        """Initialize all application resources"""
        try:
            # Initialize HTTP session
            self.http_session = aiohttp.ClientSession()
            
            # Initialize Redis if configured
            if settings.REDIS_URL:
                self.redis_client = redis.from_url(settings.REDIS_URL)
                await self.redis_client.ping()
                
            logger.info("Successfully initialized all resources")
        except Exception as e:
            logger.error(f"Failed to initialize resources: {e}")
            await self.cleanup()
            raise
            
    async def cleanup(self):
        """Cleanup all application resources"""
        try:
            if self.http_session:
                await self.http_session.close()
                
            if self.redis_client:
                await self.redis_client.close()
                
            logger.info("Successfully cleaned up all resources")
        except Exception as e:
            logger.error(f"Error during resource cleanup: {e}")
            raise

@asynccontextmanager
async def get_resource_manager() -> AsyncGenerator[ResourceManager, None]:
    """Context manager for resource management"""
    manager = ResourceManager()
    try:
        await manager.initialize()
        yield manager
    finally:
        await manager.cleanup() 