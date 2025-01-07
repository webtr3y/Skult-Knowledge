import discord
from discord.ext import commands, tasks
import requests
import os
from dotenv import load_dotenv
import snscrape.modules.twitter as sntwitter

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
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("Hello, I'm online and ready!")

# Magic Eden API Integration
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

def fetch_magic_eden_activities(collection_symbol):
    """Fetch recent NFT collection activities from Magic Eden."""
    try:
        url = f"{MAGIC_EDEN_BASE_URL}/collections/{collection_symbol}/activities"
        response = requests.get(url, headers=get_magic_eden_headers())
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching activities for {collection_symbol}: {e}")
        return []

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

@bot.command()
async def recent_activities(ctx, collection_symbol: str):
    """Display recent Magic Eden collection activities."""
    activities = fetch_magic_eden_activities(collection_symbol)
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
        message += f"- {name}: ${price:.2f}\n"

    await ctx.send(message)

# Twitter Data with snscrape
@bot.command()
async def nft_tweets(ctx, keyword: str):
    """Fetches recent tweets about NFTs with a given keyword."""
    try:
        tweets = []
        for tweet in sntwitter.TwitterSearchScraper(f'{keyword} NFT').get_items():
            if len(tweets) == 5:  # Limit to 5 tweets
                break
            tweets.append(f"{tweet.content} - {tweet.date} by {tweet.user.username}")
        
        if tweets:
            await ctx.send("**Recent NFT Tweets:**\n" + "\n\n".join(tweets))
        else:
            await ctx.send(f"No tweets found for '{keyword}' in the NFT space.")
    except Exception as e:
        await ctx.send(f"Error fetching tweets: {e}")

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
        activities = fetch_magic_eden_activities(collection)

        if stats:
            message += (
                f"\n**{collection}**\n"
                f"- Floor Price: {stats['floor_price']:.2f} SOL\n"
                f"- Volume: {stats['volume_all_time']:.2f} SOL\n"
                f"- Listed Count: {stats['listed_count']}\n"
            )

        if activities:
            message += "**Recent Activities:**\n"
            for activity in activities[:3]:  # Limit to 3 activities
                tx_type = activity.get("type", "Unknown")
                price = activity.get("price", 0) / 1e9
                message += f"- Type: {tx_type}, Price: {price:.2f} SOL\n"

    await channel.send(message)

# Start the daily updates
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    daily_update.start()

# Run the bot
bot.run(TOKEN)
