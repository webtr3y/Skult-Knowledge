from typing import Dict, List, Optional
from datetime import datetime, timedelta
import asyncio
from loguru import logger

class DeFiAnalytics:
    def __init__(self):
        self.protocol_cache = {}
        self.update_interval = timedelta(minutes=5)
        self.last_update = {}

    async def get_protocol_metrics(self, protocol: str) -> Dict:
        """Get comprehensive protocol metrics"""
        try:
            if await self.should_update(protocol):
                metrics = await self.fetch_fresh_metrics(protocol)
                self.protocol_cache[protocol] = {
                    'data': metrics,
                    'timestamp': datetime.now()
                }
            
            return self.protocol_cache[protocol]['data']
        except Exception as e:
            logger.error(f"Error fetching protocol metrics: {str(e)}")
            return {}

    async def analyze_yield_opportunities(self, protocol: str) -> List[Dict]:
        """Analyze and rank yield opportunities"""
        try:
            pools = await self.get_protocol_pools(protocol)
            return [
                {
                    'pool': pool['name'],
                    'apy': pool['apy'],
                    'tvl': pool['tvl'],
                    'risk_score': await self.calculate_risk_score(pool),
                    'recommendation': self.generate_recommendation(pool)
                }
                for pool in pools
            ]
        except Exception as e:
            logger.error(f"Error analyzing yield opportunities: {str(e)}")
            return []

    async def calculate_risk_score(self, pool: Dict) -> float:
        """Calculate risk score for a pool"""
        factors = {
            'tvl': 0.3,
            'volatility': 0.2,
            'protocol_age': 0.15,
            'audit_score': 0.2,
            'complexity': 0.15
        }
        
        scores = await self.get_risk_factors(pool)
        return sum(scores[factor] * weight for factor, weight in factors.items())

    def generate_recommendation(self, pool: Dict) -> str:
        """Generate personalized pool recommendations"""
        if pool['risk_score'] < 0.3:
            return "🟢 Solid yield opportunity for beginners"
        elif pool['risk_score'] < 0.6:
            return "🟡 Decent returns but DYOR"
        else:
            return "🔴 High risk, high reward. Degens only!" 