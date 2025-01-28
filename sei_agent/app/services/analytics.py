from typing import Dict, List
from datetime import datetime
import pandas as pd

class AnalyticsService:
    def __init__(self):
        self.price_tracker = PriceAnalytics()
        self.network_monitor = NetworkAnalytics()
        self.social_analyzer = SocialAnalytics()
        self.protocol_tracker = ProtocolAnalytics()

    async def generate_hourly_report(self) -> Dict:
        """Generate comprehensive hourly analytics"""
        return {
            'price_metrics': await self.price_tracker.get_metrics(),
            'network_health': await self.network_monitor.get_status(),
            'social_sentiment': await self.social_analyzer.get_sentiment(),
            'protocol_stats': await self.protocol_tracker.get_stats()
        }

    async def identify_market_gaps(self) -> List[Dict]:
        """Analyze ecosystem for opportunities"""
        return await self.protocol_tracker.find_opportunities() 