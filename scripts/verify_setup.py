"""
Setup Verification Script

This script verifies that all components are properly configured and working.
"""

import sys
import os
from pathlib import Path
import asyncio
from loguru import logger

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from app.config.settings import settings
from app.utils.resource_manager import ResourceManager
from app.services.twitter import TwitterService
from app.services.blockchain import BlockchainService

async def verify_setup():
    """Verify all components are properly configured"""
    try:
        logger.info("Starting setup verification...")
        
        # Check environment variables
        logger.info("Checking environment variables...")
        required_vars = [
            'TWITTER_API_KEY',
            'TWITTER_API_SECRET',
            'TWITTER_ACCESS_TOKEN',
            'TWITTER_ACCESS_TOKEN_SECRET',
            'SECRET_KEY'
        ]
        
        missing_vars = [var for var in required_vars if not getattr(settings, var, None)]
        if missing_vars:
            logger.error(f"Missing required environment variables: {missing_vars}")
            return False
            
        # Initialize resource manager
        logger.info("Initializing resource manager...")
        resource_manager = ResourceManager()
        await resource_manager.initialize()
        
        # Test Twitter service
        logger.info("Testing Twitter service...")
        twitter_service = TwitterService()
        await twitter_service.verify_credentials()
        
        # Test blockchain service
        logger.info("Testing blockchain service...")
        blockchain_service = BlockchainService()
        await blockchain_service.verify_connection()
        
        # Cleanup
        await resource_manager.cleanup()
        
        logger.success("All components verified successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Setup verification failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(verify_setup())
    sys.exit(0 if success else 1) 