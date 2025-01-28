import snscrape.modules.twitter as sntwitter
from typing import Dict, List, Optional
import logging
from datetime import datetime, timedelta

class SEITrendAnalyzer:
    def __init__(self):
        # SEI-specific keywords
        self.tracked_keywords = [
            "SEI", "SEI Network", "SEINetwork",
            "SEI NFT", "SEI DeFi", "$SEI",
            "SEI Protocol", "SEI Ecosystem"
        ]
        
        # SEI-specific NFT collections on Magic Eden
        self.sei_collections = [
            "sei_bears",
            # Add more collections as they launch
        ]
        
        # SEI DeFi protocols
        self.defi_protocols = [
            "astroport_sei",
            "levana",
            # Add more protocols
        ]
        
        self.logger = logging.getLogger(__name__)

    def analyze_sei_trends(self, hours_back: int = 24) -> Dict:
        """Analyze SEI-specific trends"""
        try:
            trends = {
                'social': self._analyze_social_trends(hours_back),
                'nft': self._analyze_nft_trends(),
                'defi': self._analyze_defi_trends()
            }
            return trends
        except Exception as e:
            self.logger.error(f"Error analyzing SEI trends: {str(e)}")
            return {}

    def generate_update_tweet(self, trends: Dict) -> str:
        """Generate a tweet about current SEI trends"""
        try:
            # Find the most significant trend
            social_trend = trends.get('social', {})
            nft_trend = trends.get('nft', {})
            
            tweet_templates = [
                "🔥 SEI Network Update 🔥\n\n"
                "📊 Most discussed: {topic}\n"
                "💬 {mention_count} mentions\n"
                "📈 Engagement: {engagement}\n\n"
                "#SEI #Crypto",

                "👾 SEI NFT Alert!\n\n"
                "🎯 Top collection: {collection}\n"
                "💎 Floor: {floor_price}\n"
                "📊 24h Volume: {volume}\n\n"
                "#SEI #NFTs",
            ]
            
            # Choose template based on what's most interesting
            # Implementation will vary based on the data we get
            
            return tweet_templates[0].format(
                topic="SEI DeFi",
                mention_count=social_trend.get('mention_count', 0),
                engagement="High"
            )
            
        except Exception as e:
            self.logger.error(f"Error generating tweet: {str(e)}")
            return "🔥 SEI Network is buzzing! Check out the latest updates. #SEI #Crypto"

    def analyze_social_trends(self, hours_back: int = 24) -> Dict:
        """
        Analyze recent social media trends for crypto-related topics
        
        Args:
            hours_back (int): Hours of historical data to analyze
            
        Returns:
            Dict: Analyzed trends for each keyword
        """
        try:
            trends = {}
            since_time = datetime.now() - timedelta(hours=hours_back)
            
            for keyword in self.tracked_keywords:
                query = f"{keyword} since:{since_time.strftime('%Y-%m-%d')}"
                tweets = sntwitter.TwitterSearchScraper(query).get_items()
                
                mentions = self._collect_mentions(tweets)
                trends[keyword] = self._process_mentions(mentions)
                
            return trends
            
        except Exception as e:
            self.logger.error(f"Error analyzing trends: {str(e)}")
            return {}
    
    def _collect_mentions(self, tweets) -> List[Dict]:
        """Collect and structure tweet data"""
        mentions = []
        try:
            for tweet in list(tweets)[:100]:
                mentions.append({
                    'text': tweet.content,
                    'date': tweet.date,
                    'engagement': tweet.likeCount + tweet.retweetCount,
                    'sentiment': None  # Will be filled by sentiment analyzer
                })
        except Exception as e:
            self.logger.error(f"Error collecting mentions: {str(e)}")
        
        return mentions
    
    def _process_mentions(self, mentions: List[Dict]) -> Optional[Dict]:
        """Process collected mentions to identify trends"""
        if not mentions:
            return None
            
        try:
            total_engagement = sum(mention['engagement'] for mention in mentions)
            avg_engagement = total_engagement / len(mentions)
            
            # Calculate hourly mention velocity
            mention_times = [mention['date'] for mention in mentions]
            time_range = max(mention_times) - min(mention_times)
            mentions_per_hour = len(mentions) / (time_range.total_seconds() / 3600)
            
            return {
                'mention_count': len(mentions),
                'avg_engagement': avg_engagement,
                'mentions_per_hour': mentions_per_hour,
                'sentiment_distribution': {
                    'positive': 0,  # Will be updated by sentiment analyzer
                    'neutral': 0,
                    'negative': 0
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error processing mentions: {str(e)}")
            return None 