import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Twitter API Credentials
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    # Magic Eden API
    MAGIC_EDEN_API_KEY = os.getenv('MAGIC_EDEN_API_KEY')

    # Application Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    TWEET_INTERVAL_HOURS = 9  # Time between tweets (8am to 5pm) 