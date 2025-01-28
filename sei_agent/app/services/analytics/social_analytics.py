from typing import Dict, List, Optional
from datetime import datetime, timedelta
import tweepy
from textblob import TextBlob
import asyncio
from loguru import logger
from ...config.settings import Settings

class SocialAnalytics:
    def __init__(self):
        self.settings = Settings()
        self.twitter_api = self.setup_twitter_api()
        self.sentiment_cache = {}
        self.keywords = [
            'SEI Network', '$SEI', 'SEI Protocol',
            'SEI DeFi', 'SEI NFT', 'SEI Ecosystem'
        ]
        
    def setup_twitter_api(self) -> tweepy.API:
        """Initialize Twitter API client"""
        auth = tweepy.OAuthHandler(
            self.settings.TWITTER_API_KEY.get_secret_value(),
            self.settings.TWITTER_API_SECRET.get_secret_value()
        )
        auth.set_access_token(
            self.settings.TWITTER_ACCESS_TOKEN.get_secret_value(),
            self.settings.TWITTER_ACCESS_TOKEN_SECRET.get_secret_value()
        )
        return tweepy.API(auth, wait_on_rate_limit=True)

    async def get_recent_mentions(self, hours: int = 24) -> List[Dict]:
        """Get recent mentions of SEI"""
        try:
            mentions = []
            since_time = datetime.utcnow() - timedelta(hours=hours)
            
            for keyword in self.keywords:
                tweets = self.twitter_api.search_tweets(
                    q=keyword,
                    lang="en",
                    count=100,
                    tweet_mode="extended"
                )
                
                for tweet in tweets:
                    if tweet.created_at >= since_time:
                        mentions.append({
                            'id': tweet.id,
                            'text': tweet.full_text,
                            'user': tweet.user.screen_name,
                            'created_at': tweet.created_at,
                            'retweets': tweet.retweet_count,
                            'likes': tweet.favorite_count
                        })
            
            return mentions
        except Exception as e:
            logger.error(f"Error getting mentions: {str(e)}")
            return []

    async def calculate_overall_sentiment(self, mentions: List[Dict]) -> Dict:
        """Calculate overall sentiment from mentions"""
        try:
            if not mentions:
                return {'positive': 0, 'neutral': 0, 'negative': 0}
            
            sentiments = {'positive': 0, 'neutral': 0, 'negative': 0}
            
            for mention in mentions:
                sentiment = self.analyze_text_sentiment(mention['text'])
                if sentiment > 0:
                    sentiments['positive'] += 1
                elif sentiment < 0:
                    sentiments['negative'] += 1
                else:
                    sentiments['neutral'] += 1
            
            total = len(mentions)
            return {
                'positive': round(sentiments['positive'] / total * 100, 2),
                'neutral': round(sentiments['neutral'] / total * 100, 2),
                'negative': round(sentiments['negative'] / total * 100, 2)
            }
        except Exception as e:
            logger.error(f"Error calculating sentiment: {str(e)}")
            return {'positive': 0, 'neutral': 0, 'negative': 0}

    def analyze_text_sentiment(self, text: str) -> float:
        """Analyze sentiment of text using TextBlob"""
        try:
            analysis = TextBlob(text)
            return analysis.sentiment.polarity
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return 0.0

    async def get_trending_topics(self) -> List[Dict]:
        """Get trending topics related to SEI"""
        try:
            mentions = await self.get_recent_mentions(hours=24)
            topics = {}
            
            for mention in mentions:
                words = mention['text'].lower().split()
                for word in words:
                    if word.startswith('#'):
                        topics[word] = topics.get(word, 0) + 1
            
            sorted_topics = sorted(
                topics.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10]
            
            return [
                {'topic': topic, 'mentions': count}
                for topic, count in sorted_topics
            ]
        except Exception as e:
            logger.error(f"Error getting trending topics: {str(e)}")
            return []

    async def get_community_growth(self) -> Dict:
        """Get community growth metrics"""
        try:
            user = self.twitter_api.get_user(screen_name="SeiNetwork")
            current_followers = user.followers_count
            
            # Get historical data from cache/database
            # For MVP, we'll return basic metrics
            return {
                'followers': current_followers,
                'growth_rate': 0,  # To be implemented with historical data
                'engagement_rate': await self.calculate_engagement_rate()
            }
        except Exception as e:
            logger.error(f"Error getting community growth: {str(e)}")
            return {'followers': 0, 'growth_rate': 0, 'engagement_rate': 0}

    async def calculate_engagement_rate(self) -> float:
        """Calculate engagement rate"""
        try:
            mentions = await self.get_recent_mentions(hours=24)
            if not mentions:
                return 0.0
            
            total_engagement = sum(
                mention['retweets'] + mention['likes']
                for mention in mentions
            )
            
            return round(total_engagement / len(mentions), 2)
        except Exception as e:
            logger.error(f"Error calculating engagement rate: {str(e)}")
            return 0.0

    async def get_sentiment(self) -> Dict:
        """Get social sentiment analysis"""
        mentions = await self.get_recent_mentions()
        return {
            'overall_sentiment': await self.calculate_overall_sentiment(mentions),
            'engagement_rate': await self.calculate_engagement_rate(),
            'trending_topics': await self.get_trending_topics(),
            'community_growth': await self.get_community_growth()
        }
        
    async def analyze_community_sentiment(self, timeframe: str = '24h') -> Dict:
        """Analyze community sentiment over time"""
        posts = await self.get_community_posts(timeframe)
        return {
            'sentiment_breakdown': self.analyze_sentiment_distribution(posts),
            'key_topics': await self.extract_key_topics(posts),
            'influential_posts': await self.identify_influential_posts(posts)
        }

    async def track_social_metrics(self) -> Dict:
        """Track key social metrics"""
        return {
            'follower_growth': await self.get_follower_growth_rate(),
            'engagement_metrics': await self.get_engagement_metrics(),
            'reach_metrics': await self.get_reach_metrics()
        } 