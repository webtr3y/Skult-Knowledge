from discord.ext import commands
import snscrape.modules.twitter as sntwitter
from textblob import TextBlob

def analyze_sentiment(keyword):
    """Fetch recent tweets and analyze sentiment."""
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(f'{keyword}').get_items():
        if len(tweets) == 10:  # Analyze the latest 10 tweets
            break
        tweets.append(tweet.content)
    
    sentiments = {"positive": 0, "negative": 0, "neutral": 0}
    for tweet in tweets:
        sentiment = TextBlob(tweet).sentiment.polarity
        if sentiment > 0:
            sentiments["positive"] += 1
        elif sentiment < 0:
            sentiments["negative"] += 1
        else:
            sentiments["neutral"] += 1
    
    return sentiments

class SocialSentiment(commands.Cog):
    """Commands for social sentiment analysis."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sentiment(self, ctx, keyword: str):
        """Analyze and report sentiment on a given keyword."""
        sentiments = analyze_sentiment(keyword)
        await ctx.send(
            f"Sentiment for '{keyword}':\n"
            f"- Positive: {sentiments['positive']}\n"
            f"- Negative: {sentiments['negative']}\n"
            f"- Neutral: {sentiments['neutral']}"
        )

@bot.command(name="social_sentiment")
async def social_sentiment(ctx, keyword: str):
    sentiment_data = fetch_twitter_sentiment(keyword)  # Replace with actual Twitter API or snscrape logic
    await ctx.send(f"Sentiment for {keyword}: {sentiment_data}")


def setup(bot):
    bot.add_cog(SocialSentiment(bot))
