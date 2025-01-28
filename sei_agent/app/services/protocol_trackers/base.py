from typing import Dict, List
from abc import ABC, abstractmethod

class BaseProtocolTracker(ABC):
    @abstractmethod
    async def get_stats(self) -> Dict:
        """Get protocol statistics"""
        pass
    
    @abstractmethod
    async def analyze_trends(self) -> Dict:
        """Analyze protocol trends"""
        pass

class AstroportTracker(BaseProtocolTracker):
    async def get_stats(self) -> Dict:
        """Get Astroport statistics"""
        return {
            'tvl': await self.get_tvl(),
            'volume_24h': await self.get_24h_volume(),
            'pools': await self.get_pool_metrics(),
            'users': await self.get_user_metrics()
        }

    async def analyze_trends(self) -> Dict:
        """Analyze Astroport trends"""
        return {
            'volume_trend': await self.analyze_volume_trend(),
            'tvl_trend': await self.analyze_tvl_trend(),
            'user_growth': await self.analyze_user_growth()
        } 