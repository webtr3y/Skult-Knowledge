from typing import List, Dict

class MarketAnalysisService:
    async def analyze_market_gaps(self) -> List[Dict]:
        """Identify market opportunities"""
        return {
            'defi_gaps': await self.analyze_defi_opportunities(),
            'infrastructure_needs': await self.analyze_infrastructure(),
            'user_demands': await self.analyze_community_needs()
        }

    async def generate_market_insight(self) -> str:
        """Generate market insight content"""
        data = await self.gather_market_data()
        return self.format_market_insight(data) 