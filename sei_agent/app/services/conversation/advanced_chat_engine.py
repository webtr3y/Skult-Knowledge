from typing import Dict, List, Optional, Tuple
import re
from loguru import logger
from .patterns import CONVERSATION_PATTERNS
from ..analytics.network_analytics import NetworkAnalytics
from ..analytics.social_analytics import SocialAnalytics
from .eliza_patterns import ElizaPatternMatcher
import random

class AdvancedSEIConversationEngine:
    def __init__(self):
        self.patterns = CONVERSATION_PATTERNS
        self.context = {}
        self.network_analytics = NetworkAnalytics()
        self.social_analytics = SocialAnalytics()
        self.conversation_history = []
        self.eliza_matcher = ElizaPatternMatcher()
        
    async def process_message(self, message: str, user_id: str = "default") -> Dict:
        """Process message using ELIZA patterns first, then domain-specific logic"""
        try:
            # Try ELIZA-style pattern matching first
            if eliza_response := self.eliza_matcher.match_pattern(message):
                response = self.format_eliza_response(eliza_response)
                return await self.enhance_with_data(response)
                
            # Fall back to domain-specific patterns
            return await self.match_and_respond(message)
            
        except Exception as e:
            logger.error(f"Error in conversation processing: {str(e)}")
            return self.generate_fallback_response()
            
    async def match_and_respond(self, message: str) -> Dict:
        """Match message against patterns and generate response"""
        message = message.lower()
        
        for pattern, handlers in self.patterns.items():
            if match := re.search(pattern, message):
                response_func = handlers['response_func']
                response = await response_func(self, match)
                return {
                    'response': response['text'],
                    'follow_up': response.get('follow_up', []),
                    'data': response.get('data', {}),
                    'sentiment': response.get('sentiment', 'neutral')
                }
                
        return await self.generate_default_response(message)
        
    def update_context(self, message: str, user_id: str):
        """Update conversation context"""
        if user_id not in self.context:
            self.context[user_id] = {
                'topics_discussed': set(),
                'questions_asked': [],
                'sentiment': 'neutral',
                'expertise_level': 'beginner',
                'last_interaction': None
            }
            
        context = self.context[user_id]
        context['last_interaction'] = datetime.now()
        
        # Update topics discussed
        for topic in ['defi', 'trading', 'development', 'network']:
            if topic in message.lower():
                context['topics_discussed'].add(topic)
                
        # Update expertise level based on conversation
        if any(term in message.lower() for term in ['code', 'develop', 'smart contract']):
            context['expertise_level'] = 'advanced'
            
    async def enhance_with_data(self, response: Dict) -> Dict:
        """Enhance response with real-time data"""
        if 'network_stats' in response.get('data_requirements', []):
            stats = await self.network_analytics.get_status()
            response['data']['network'] = stats
            
        if 'social_metrics' in response.get('data_requirements', []):
            metrics = await self.social_analytics.get_sentiment()
            response['data']['social'] = metrics
            
        return response
        
    def generate_fallback_response(self) -> Dict:
        """Generate fallback response for error cases"""
        return {
            'response': "I'm here to help with SEI Network information. Would you like to know about the current network status or learn about specific features?",
            'follow_up': [
                "Show network status",
                "Learn about SEI features",
                "Get started with SEI"
            ],
            'data': {}
        }

    async def handle_context_based_response(self, user_id: str) -> Optional[Dict]:
        """Handle responses based on conversation context"""
        if user_id not in self.context:
            return None
            
        context = self.context[user_id]
        
        # Handle follow-ups based on expertise level
        if context['expertise_level'] == 'advanced':
            return await self.generate_advanced_response(context)
        
        # Handle based on topics discussed
        if 'defi' in context['topics_discussed']:
            return await self.generate_defi_focused_response(context)
            
        return None 

    def format_eliza_response(self, eliza_match: Dict) -> Dict:
        """Format ELIZA-style response with blockchain context"""
        template = random.choice(eliza_match['response_template'])
        response = template.format(**eliza_match['variables'])
        
        return {
            'response': response,
            'follow_up': self.generate_follow_up(eliza_match['variables']),
            'data_requirements': ['network_stats'] if 'network' in str(eliza_match['variables']) else []
        } 