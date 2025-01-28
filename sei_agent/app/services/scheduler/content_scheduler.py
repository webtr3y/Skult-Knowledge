from typing import Dict, List
from datetime import datetime, timedelta
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class ContentScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.content_queue = []
        
    async def initialize(self):
        """Initialize scheduler with default jobs"""
        self.scheduler.add_job(
            self.post_hourly_update,
            'interval',
            hours=1,
            next_run_time=datetime.now()
        )
        
        self.scheduler.add_job(
            self.post_daily_analysis,
            'cron',
            hour=12  # UTC time
        )
        
        self.scheduler.start()
        
    async def schedule_content(self, content_type: str, content: Dict, timestamp: datetime):
        """Schedule content for posting"""
        self.content_queue.append({
            'type': content_type,
            'content': content,
            'timestamp': timestamp
        })
        
    async def post_hourly_update(self):
        """Post hourly ecosystem update"""
        content = await self.generate_hourly_content()
        await self.social_engagement.post_content(content) 