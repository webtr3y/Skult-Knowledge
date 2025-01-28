from typing import Dict, List, Optional
from datetime import datetime
from loguru import logger
from .analytics.social_analytics import SocialAnalytics
from .analytics.network_analytics import NetworkAnalytics
from .protocol_trackers.base import AstroportTracker
from .conversation.chat_engine import SEIConversationEngine
from .conversation.advanced_chat_engine import AdvancedSEIConversationEngine

class ContentGenerator:
    def __init__(self):
        self.social_analytics = SocialAnalytics()
        self.network_analytics = NetworkAnalytics()
        self.protocol_tracker = AstroportTracker()
        self.content_types = {
            'network_update': self.generate_network_update,
            'market_analysis': self.generate_market_analysis,
            'educational': self.generate_educational_content,
            'community': self.generate_community_update
        }

    async def generate_hourly_content(self) -> Dict:
        """Generate content for hourly updates"""
        try:
            network_stats = await self.network_analytics.get_status()
            social_stats = await self.social_analytics.get_sentiment()
            
            content = {
                'title': '🔄 Hourly SEI Network Update',
                'network_metrics': self.format_network_metrics(network_stats),
                'social_insights': self.format_social_insights(social_stats),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            return self.format_tweet_thread(content)
        except Exception as e:
            logger.error(f"Error generating hourly content: {str(e)}")
            return self.generate_fallback_content()

    def format_network_metrics(self, stats: Dict) -> List[str]:
        """Format network metrics for Twitter"""
        return [
            f"📊 Network Stats:",
            f"• TPS: {stats['tps']:.2f}",
            f"• Active Validators: {stats['validators']['active_validators']}",
            f"• Network Health: {stats['network_health']['status'].title()}"
        ]

    def format_social_insights(self, stats: Dict) -> List[str]:
        """Format social insights for Twitter"""
        sentiment = stats['overall_sentiment']
        return [
            f"👥 Community Pulse:",
            f"• Sentiment: {'📈' if sentiment['positive'] > 30 else '📉'}",
            f"• Engagement Rate: {stats['engagement_rate']}%",
            f"• Top Trend: {stats['trending_topics'][0]['topic'] if stats['trending_topics'] else 'N/A'}"
        ]

    def format_tweet_thread(self, content: Dict) -> List[str]:
        """Format content into tweet thread"""
        thread = []
        
        # Main tweet
        thread.append(f"{content['title']}\n\n" + "\n".join(content['network_metrics']))
        
        # Social insights
        thread.append("\n".join(content['social_insights']))
        
        # Call to action
        thread.append("🔔 Follow @SeiNetwork for more updates!\n#SEI #Crypto #DeFi")
        
        return thread

    async def generate_educational_content(self, topic: str) -> List[str]:
        """Generate educational content thread"""
        topics = {
            'basics': self.generate_sei_basics,
            'defi': self.generate_defi_guide,
            'ecosystem': self.generate_ecosystem_overview
        }
        
        generator = topics.get(topic, self.generate_sei_basics)
        return await generator()

    async def generate_sei_basics(self) -> List[str]:
        """Generate basic SEI educational content"""
        return [
            "🎓 SEI Network Basics - A Thread 🧵\n\nSEI is a specialized Layer 1 blockchain optimized for trading...",
            "1️⃣ Key Features:\n• Parallel execution\n• Built-in orderbook\n• Fast finality\n• Low fees",
            "2️⃣ Why SEI?\n• Designed for DeFi\n• Superior trading experience\n• Growing ecosystem",
            "3️⃣ Getting Started:\n• Get a wallet\n• Bridge assets\n• Explore DApps",
            "🌟 Want to learn more? Follow us and check out docs.sei.io!\n#SEI #Crypto #DeFi"
        ]

    def generate_fallback_content(self) -> List[str]:
        """Generate fallback content when main generation fails"""
        return [
            "🔄 SEI Network Update\n\nStay tuned for our next detailed update!",
            "Follow @SeiNetwork for the latest news and insights!\n#SEI #Crypto"
        ]

    async def initialize(self):
        """Initialize required services"""
        await self.network_analytics.initialize()

    async def cleanup(self):
        """Cleanup resources"""
        await self.network_analytics.cleanup()

    async def create_educational_thread(self, topic: str) -> List[str]:
        """Create educational thread with consistent branding"""
        template = self.brand_voice.get_thread_template()
        return await self.format_educational_content(topic, template)

    async def generate_chat_response(self, message: str, user_id: str = "default") -> Dict:
        """Generate enhanced conversational response"""
        chat_engine = AdvancedSEIConversationEngine()
        
        # Process message with context
        response = await chat_engine.process_message(message, user_id)
        
        # Enhance with additional data if needed
        if 'data' in response:
            network_stats = await self.network_analytics.get_status()
            social_stats = await self.social_analytics.get_sentiment()
            response['data'].update({
                'network': network_stats,
                'social': social_stats
            })
        
        return response 