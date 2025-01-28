from typing import Dict, List
from datetime import datetime, timedelta
import asyncio
from loguru import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from .content_generator import ContentGenerator
from .twitter import TwitterService

class ContentScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.content_generator = ContentGenerator()
        self.twitter_service = TwitterService()
        self.scheduled_jobs = {}

    async def initialize(self):
        """Initialize scheduler and services"""
        await self.content_generator.initialize()
        await self.twitter_service.verify_credentials()
        
        # Schedule hourly updates
        self.scheduler.add_job(
            self.post_hourly_update,
            'interval',
            hours=1,
            id='hourly_update',
            next_run_time=datetime.now()
        )
        
        # Schedule daily analysis
        self.scheduler.add_job(
            self.post_daily_analysis,
            CronTrigger(hour=0, minute=0),
            id='daily_analysis'
        )
        
        # Schedule educational content
        self.scheduler.add_job(
            self.post_educational_content,
            CronTrigger(hour=12, minute=0),
            id='educational_content'
        )
        
        self.scheduler.start()
        logger.info("Content scheduler initialized")

    async def post_hourly_update(self):
        """Post hourly network update"""
        try:
            content = await self.content_generator.generate_hourly_content()
            for tweet in content:
                await self.twitter_service.post_tweet(tweet)
            logger.info("Posted hourly update")
        except Exception as e:
            logger.error(f"Error posting hourly update: {str(e)}")

    async def post_daily_analysis(self):
        """Post daily network analysis"""
        try:
            # Implementation for daily analysis
            pass
        except Exception as e:
            logger.error(f"Error posting daily analysis: {str(e)}")

    async def post_educational_content(self):
        """Post educational content"""
        try:
            topics = ['basics', 'defi', 'ecosystem']
            topic = topics[datetime.now().day % len(topics)]
            content = await self.content_generator.generate_educational_content(topic)
            await self.twitter_service.post_thread(content)
            logger.info(f"Posted educational content about {topic}")
        except Exception as e:
            logger.error(f"Error posting educational content: {str(e)}")

    async def cleanup(self):
        """Cleanup resources"""
        self.scheduler.shutdown()
        await self.content_generator.cleanup()
        logger.info("Content scheduler shutdown") 