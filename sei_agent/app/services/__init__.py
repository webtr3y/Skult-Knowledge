"""
Services Package

Initializes all service components.
"""

from .blockchain import BlockchainService
from .twitter import TwitterService
from .content_generator import ContentGenerator
from .scheduler import ContentScheduler
from .analytics.network_analytics import NetworkAnalytics
from .analytics.social_analytics import SocialAnalytics
from .protocol_trackers.base import AstroportTracker
from .defi_educator import DeFiEducator
from .nft_tracker import NFTTracker

__all__ = [
    'BlockchainService',
    'TwitterService',
    'NFTTracker',
    'DeFiEducator',
    'AstroportTracker'
]

class ServiceManager:
    """Manages all service instances and their lifecycle"""
    def __init__(self):
        self.blockchain = BlockchainService()
        self.twitter = TwitterService()
        self.content_generator = ContentGenerator()
        self.scheduler = ContentScheduler()
        self.network_analytics = NetworkAnalytics()
        self.social_analytics = SocialAnalytics()
        self.defi_educator = DeFiEducator()
        self.nft_tracker = NFTTracker()
        
    async def initialize(self):
        """Initialize all services"""
        await self.blockchain.initialize()
        await self.twitter.verify_credentials()
        await self.content_generator.initialize()
        await self.scheduler.initialize()
        
    async def cleanup(self):
        """Cleanup all services"""
        await self.scheduler.cleanup()
        await self.content_generator.cleanup()
        await self.blockchain.cleanup()

# Initialize service components 