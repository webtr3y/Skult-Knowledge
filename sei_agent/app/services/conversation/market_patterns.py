"""
Market-specific conversation patterns extending ELIZA framework.
"""

from typing import Dict, List
import re

class MarketPatternMatcher:
    def __init__(self):
        self.market_patterns = {
            # Price analysis patterns
            r'.*why (is|did) (.*) (going|went) (up|down)': {
                'decomposition': ['tense', 'asset', 'direction', 'movement'],
                'reassembly': [
                    "Let's analyze the factors affecting {asset}. Would you like to see the key metrics?",
                    "There are several factors influencing {asset}'s price. Should we look at the data?",
                    "I can help you understand {asset}'s price movement. Where would you like to start?"
                ],
                'data_requirements': ['price_history', 'market_events', 'social_sentiment']
            },

            # Trading strategy patterns
            r'.*how (can|do) i (trade|invest in) (.*)': {
                'decomposition': ['intent', 'action', 'asset'],
                'reassembly': [
                    "Before trading {asset}, let's review some important principles. What's your experience level?",
                    "Trading {asset} requires understanding several key concepts. Shall we start with the basics?",
                    "I can guide you through {asset} trading strategies. Would you like to begin with risk management?"
                ],
                'educational_path': 'trading_basics'
            },

            # Risk assessment patterns
            r'.*what (are|is) the (risks?|downsides?) of (.*)': {
                'decomposition': ['tense', 'concern', 'topic'],
                'reassembly': [
                    "Understanding the risks of {topic} is crucial. Let me show you some key considerations.",
                    "There are several important factors to consider with {topic}. Should we analyze them together?",
                    "Risk assessment for {topic} involves multiple aspects. Where would you like to focus?"
                ],
                'data_requirements': ['risk_metrics', 'historical_data']
            }
        }

    async def process_market_query(self, message: str, user_context: Dict) -> Dict:
        """Process market-related queries with context awareness"""
        for pattern, response_data in self.market_patterns.items():
            if match := re.match(pattern, message, re.I):
                return await self.generate_market_response(match, response_data, user_context)
        return None

    async def generate_market_response(self, match: re.Match, response_data: Dict, user_context: Dict) -> Dict:
        """Generate contextual market-focused response"""
        variables = dict(zip(response_data['decomposition'], match.groups()))
        
        # Enhance response based on user's expertise level
        expertise_level = user_context.get('expertise_level', 'beginner')
        response = self.adapt_to_expertise(response_data['reassembly'], expertise_level)
        
        return {
            'response': response.format(**variables),
            'data_requirements': response_data.get('data_requirements', []),
            'educational_path': response_data.get('educational_path'),
            'context_update': {'last_topic': variables.get('topic', '')}
        } 