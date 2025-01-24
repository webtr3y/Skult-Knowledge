import discord
from discord.ext import commands, tasks
import requests
import os
from dotenv import load_dotenv
import snscrape.modules.twitter as sntwitter
import ssl
import certifi

# Fix SSL Context
ssl._create_default_https_context = ssl._create_unverified_context
ssl.create_default_context(cafile=certifi.where())

print("Starting the bot...")

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
MAGIC_EDEN_API_KEY = os.getenv("MAGIC_EDEN_API_KEY")

if not TOKEN or not CHANNEL_ID or not COINMARKETCAP_API_KEY or not MAGIC_EDEN_API_KEY:
    raise ValueError("One or more required environment variables are missing in the .env file.")

CHANNEL_ID = int(CHANNEL_ID)  # Convert channel ID to integer

# Initialize bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.presences = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Ping command - test if the bot is online
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong! I am fully operational.")


# Dynamically load all command files
for filename in os.listdir("./commands"):
    if filename.endswith(".py") and not filename.startswith("__"):
        bot.load_extension(f"commands.{filename[:-3]}")

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("Hello, I'm online and ready!")

@tasks.loop(hours=1)
async def hourly_market_update():
    channel = bot.get_channel(CHANNEL_ID)
    market_trends = gnosis_agent.get_market_trends()  # AI/analytics logic
    await channel.send(f"Hourly Market Trends:\n{market_trends}")


# Magic Eden Integration
MAGIC_EDEN_BASE_URL = "https://api-mainnet.magiceden.dev/v2"

def get_magic_eden_headers():
    return {
        "Authorization": f"Bearer {MAGIC_EDEN_API_KEY}",
        "Accept": "application/json"
    }

def fetch_magic_eden_stats(collection_symbol):
    """Fetch NFT collection stats from Magic Eden."""
    try:
        url = f"{MAGIC_EDEN_BASE_URL}/collections/{collection_symbol}/stats"
        response = requests.get(url, headers=get_magic_eden_headers())
        response.raise_for_status()
        data = response.json()
        return {
            "floor_price": data.get("floorPrice", 0) / 1e9,
            "volume_all_time": data.get("volumeAll", 0) / 1e9,
            "listed_count": data.get("listedCount", 0),
        }
    except Exception as e:
        print(f"Error fetching stats for {collection_symbol}: {e}")
        return None

# Magic Eden Activities Endpoint
MAGIC_EDEN_ACTIVITIES_URL = "https://api-mainnet.magiceden.dev/v2/collections/{collection_symbol}/activities"

def fetch_collection_activities(collection_symbol):
    """Fetch recent activities for a collection from Magic Eden."""
    url = MAGIC_EDEN_ACTIVITIES_URL.format(collection_symbol=collection_symbol)
    headers = {"accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching activities for {collection_symbol}: {e}")
        return []

@bot.command()
async def recent_activities(ctx, collection_symbol: str):
    """Fetch and display recent activities for an NFT collection."""
    activities = fetch_collection_activities(collection_symbol)
    if not activities:
        await ctx.send(f"No activities found for collection: {collection_symbol}")
        return

    message = f"**Recent Activities for {collection_symbol}:**\n"
    for activity in activities[:5]:  # Limit to 5 activities
        tx_type = activity.get("type", "Unknown")
        price = activity.get("price", 0) / 1e9  # Convert lamports to SOL
        buyer = activity.get("buyer", "Unknown")
        seller = activity.get("seller", "Unknown")
        message += (
            f"- Type: {tx_type}, Price: {price:.2f} SOL, Buyer: {buyer}, Seller: {seller}\n"
        )

    await ctx.send(message)

@bot.command()
async def collection_stats(ctx, collection_symbol: str):
    """Display Magic Eden collection stats."""
    stats = fetch_magic_eden_stats(collection_symbol)
    if not stats:
        await ctx.send(f"Could not fetch stats for collection: {collection_symbol}")
        return

    message = (
        f"**Collection Stats for {collection_symbol}:**\n"
        f"- Floor Price: {stats['floor_price']:.2f} SOL\n"
        f"- Total Volume: {stats['volume_all_time']:.2f} SOL\n"
        f"- Listed Count: {stats['listed_count']} NFTs\n"
    )
    await ctx.send(message)

# CoinMarketCap Integration
COINMARKETCAP_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

def fetch_crypto_data(limit=10):
    """Fetch top cryptocurrencies by market cap."""
    try:
        headers = {"X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY}
        response = requests.get(COINMARKETCAP_URL, headers=headers, params={"limit": limit})
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        print(f"Error fetching cryptocurrency data: {e}")
        return []

@bot.command()
async def crypto_stats(ctx):
    """Display top cryptocurrency stats."""
    cryptos = fetch_crypto_data(limit=5)
    if not cryptos:
        await ctx.send("Could not fetch cryptocurrency data.")
        return

    message = "**Top Cryptocurrencies:**\n"
    for crypto in cryptos:
        name = crypto["name"]
        price = crypto["quote"]["USD"]["price"]
        change_24h = crypto["quote"]["USD"]["percent_change_24h"]
        message += (
            f"- {name}:\n"
            f"  - Price: ${price:.2f}\n"
            f"  - 24h Change: {change_24h:+.2f}%\n"
        )

    await ctx.send(message)

# Daily Updates
@tasks.loop(hours=24)
async def daily_update():
    """Daily summary updates."""
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Channel not found. Check the CHANNEL_ID in .env.")
        return

    collections = ["degenape", "solpunks"]
    message = "**Daily NFT Update:**\n"

    for collection in collections:
        stats = fetch_magic_eden_stats(collection)
        if stats:
            message += (
                f"\n**{collection}**\n"
                f"- Floor Price: {stats['floor_price']:.2f} SOL\n"
                f"- Volume: {stats['volume_all_time']:.2f} SOL\n"
                f"- Listed Count: {stats['listed_count']}\n"
            )

    await channel.send(message)
@tasks.loop(minutes=60)
async def hourly_update():
    """Hourly updates for sentiment, trading stats, and wallet activity."""
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Channel not found.")
        return

    keyword = "meme coin"
    sentiments = analyze_sentiment(keyword)
    sentiment_message = (
        f"Sentiment for '{keyword}':\n"
        f"- Positive: {sentiments['positive']}\n"
        f"- Negative: {sentiments['negative']}\n"
        f"- Neutral: {sentiments['neutral']}\n"
    )

    collections = ["degenape", "solpunks"]
    collection_message = "**NFT Collection Updates:**\n"
    for collection in collections:
        stats = fetch_magic_eden_stats(collection)
        if stats:
            collection_message += (
                f"- {collection}: Floor Price: {stats['floor_price']} SOL\n"
            )

    await channel.send(f"**Hourly Update:**\n{sentiment_message}\n{collection_message}")

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    daily_update.start()
    hourly_update.start()


bot.load_extension('commands.gnosis')

import os
from discord.ext import commands

# Dynamically load all command files
for filename in os.listdir("./commands"):
    if filename.endswith(".py") and not filename.startswith("__"):
        bot.load_extension(f"commands.{filename[:-3]}")

print("Loading commands...")
for filename in os.listdir("./commands"):
    if filename.endswith(".py") and not filename.startswith("__"):
        print(f"Loading {filename}")
        bot.load_extension(f"commands.{filename[:-3]}")
        

@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync slash commands
    print(f"Bot is online as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("Gnosis is now live and ready to assist!")

# Start the daily updates
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    daily_update.start()

class GnosisAgent:
    def process_query(self, question):
        return f"Here's my analysis for: {question}"

    def get_trading_tips(self):
        return "Diversify your portfolio and set stop-losses!"

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_message = message.content
    response = gnosis_agent.process_query(user_message)
    await message.channel.send(response)
    await bot.process_commands(message)  # Ensure other commands still work

class CryptoTrendAgent:
    def __init__(self):
        self.twitter_api = sntwitter
        self.tracked_keywords = [
            "crypto", "blockchain", "web3",
            "defi", "nft", "altcoin",
            "bitcoin", "ethereum"
        ]
        
    def analyze_social_trends(self, hours_back=24):
        """Analyze recent social media trends for crypto-related topics"""
        trends = {}
        for keyword in self.tracked_keywords:
            query = f"{keyword} since:{hours_back}h"
            tweets = sntwitter.TwitterSearchScraper(query).get_items()
            
            # Collect and analyze tweet data
            mentions = []
            for tweet in list(tweets)[:100]:  # Analyze last 100 tweets
                mentions.append({
                    'text': tweet.content,
                    'date': tweet.date,
                    'engagement': tweet.likeCount + tweet.retweetCount,
                    'sentiment': self._analyze_sentiment(tweet.content)
                })
            
            trends[keyword] = self._process_mentions(mentions)
        
        return trends
    
    def _analyze_sentiment(self, text):
        """Basic sentiment analysis - to be enhanced with proper NLP"""
        # Placeholder for sentiment analysis
        return 'neutral'
    
    def _process_mentions(self, mentions):
        """Process collected mentions to identify trends"""
        if not mentions:
            return None
            
        total_engagement = sum(mention['engagement'] for mention in mentions)
        avg_engagement = total_engagement / len(mentions)
        
        return {
            'mention_count': len(mentions),
            'avg_engagement': avg_engagement,
            'sentiment_distribution': {
                'positive': sum(1 for m in mentions if m['sentiment'] == 'positive'),
                'neutral': sum(1 for m in mentions if m['sentiment'] == 'neutral'),
                'negative': sum(1 for m in mentions if m['sentiment'] == 'negative')
            }
        }
    
    def generate_insight_tweet(self, trends):
        """Generate insights based on trend analysis"""
        # Find the most discussed topic
        top_trend = max(trends.items(), key=lambda x: x[1]['mention_count'])
        
        tweet = (
            f"🚨 Crypto Trend Alert 🚨\n\n"
            f"Hot topic: #{top_trend[0]}\n"
            f"- {top_trend[1]['mention_count']} mentions\n"
            f"- Avg engagement: {top_trend[1]['avg_engagement']:.1f}\n\n"
            f"#crypto #trading #analysis"
        )
        return tweet

# Run the bot
bot.run(TOKEN)

