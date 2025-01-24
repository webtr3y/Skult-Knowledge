import snscrape.modules.twitter as sntwitter
from typing import Dict, List, Optional
import logging
from datetime import datetime, timedelta

class TrendAnalyzer:
    def __init__(self):
        self.tracked_keywords = [
            "crypto", "blockchain", "web3",
            "defi", "nft", "altcoin",
            "bitcoin", "ethereum"
        ]
        self.logger = logging.getLogger(__name__)
        
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