import schedule
import time
from datetime import datetime
import logging
from ..agent.trend_analyzer import SEITrendAnalyzer
from ..agent.tweet_generator import SEITweetGenerator
import tweepy
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TweetScheduler:
    def __init__(self):
        self.trend_analyzer = SEITrendAnalyzer()
        self.tweet_generator = SEITweetGenerator()
        self.auth = tweepy.OAuthHandler(
            Config.TWITTER_API_KEY, 
            Config.TWITTER_API_SECRET
        )
        self.auth.set_access_token(
            Config.TWITTER_ACCESS_TOKEN, 
            Config.TWITTER_ACCESS_TOKEN_SECRET
        )
        self.api = tweepy.API(self.auth)

    def send_update(self):
        try:
            # Get trends and generate tweet
            trends = self.trend_analyzer.analyze_sei_trends()
            tweet = self.tweet_generator.generate_defi_update(trends)
            
            # Post tweet
            self.api.update_status(tweet)
            logger.info(f"Posted update at {datetime.now()}")
        except Exception as e:
            logger.error(f"Error sending update: {e}")

    def start(self):
        # Schedule updates for 8 AM and 5 PM EST
        schedule.every().day.at("08:00").do(self.send_update)
        schedule.every().day.at("17:00").do(self.send_update)

        logger.info("Tweet scheduler started")
        while True:
            schedule.run_pending()
            time.sleep(60) 