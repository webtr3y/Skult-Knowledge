"""
Test Configuration

Provides fixtures and configuration for testing.
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from typing import Generator, AsyncGenerator
from app.config.settings import settings
from app.utils.resource_manager import ResourceManager
from app.main import create_app

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for testing"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def resource_manager() -> AsyncGenerator[ResourceManager, None]:
    """Provide a resource manager for testing"""
    manager = ResourceManager()
    await manager.initialize()
    yield manager
    await manager.cleanup()

@pytest.fixture(scope="session")
async def test_app(resource_manager: ResourceManager):
    """Create a test application instance"""
    app = create_app()
    app.state.resource_manager = resource_manager
    return app

@pytest.fixture(scope="session")
def test_client(test_app):
    """Create a test client"""
    with TestClient(test_app) as client:
        yield client 