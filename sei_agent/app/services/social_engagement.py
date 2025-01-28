class SocialEngagementManager:
    def __init__(self):
        self.twitter = TwitterService()
        self.trend_analyzer = TrendAnalyzer()
        self.engagement_optimizer = EngagementOptimizer()

    async def schedule_hourly_content(self):
        """Schedule and optimize hourly content"""
        best_time = await self.engagement_optimizer.get_optimal_time()
        content = await self.content_generator.generate_hourly_content()
        
        return await self.twitter.schedule_tweet(content, best_time)

    async def monitor_and_engage(self):
        """Monitor SEI-related conversations and engage"""
        relevant_conversations = await self.trend_analyzer.find_relevant_discussions()
        for convo in relevant_conversations:
            if await self.should_engage(convo):
                await self.generate_engagement(convo) 