import discord
from discord.ext import commands, tasks
import requests
import os
from dotenv import load_dotenv

print("Starting the bot...")

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
MAGIC_EDEN_API_KEY = os.getenv("MAGIC_EDEN_API_KEY")

if not TOKEN or not CHANNEL_ID or not MAGIC_EDEN_API_KEY:
    raise ValueError("One or more required environment variables are missing in the .env file.")

CHANNEL_ID = int(CHANNEL_ID)  # Convert channel ID to integer

MAGIC_EDEN_URL = "https://api-mainnet.magiceden.dev/v2"

def get_headers():
    return {
        "Authorization": f"Bearer {MAGIC_EDEN_API_KEY}",
        "Accept": "application/json"
    }

def fetch_magic_eden_stats(collection_symbol):
    try:
        url = f"{MAGIC_EDEN_URL}/collections/{collection_symbol}/stats"
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        data = response.json()
        return {
            "floor_price": data.get("floorPrice", 0) / 1e9,
            "volume_all_time": data.get("volumeAll", 0) / 1e9,
            "listed_count": data.get("listedCount", 0),
        }
    except Exception as e:
        print(f"Error fetching stats for {collection_symbol}: {e}")
        return {}

def fetch_collection_activities(collection_symbol):
    try:
        url = f"{MAGIC_EDEN_URL}/collections/{collection_symbol}/activities"
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching activities for {collection_symbol}: {e}")
        return []

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

@bot.command()
async def collection_stats(ctx, collection_symbol: str):
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
    activities = fetch_collection_activities(collection_symbol)
    if not activities:
        await ctx.send(f"No activities found for collection: {collection_symbol}")
        return

    message = f"**Recent Activities for {collection_symbol}:**\n"
    for activity in activities[:5]:
        tx_type = activity.get("type", "Unknown")
        price = activity.get("price", 0) / 1e9
        buyer = activity.get("buyer", "Unknown")
        seller = activity.get("seller", "Unknown")
        message += (
            f"- Type: {tx_type}, Price: {price:.2f} SOL, Buyer: {buyer}, Seller: {seller}\n"
        )

    await ctx.send(message)

@tasks.loop(hours=24)
async def daily_update():
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Channel not found. Check the CHANNEL_ID in .env.")
        return

    collections = ["degenape", "solpunks"]
    message = "**Daily NFT Update:**\n"

    for collection in collections:
        stats = fetch_magic_eden_stats(collection)
        activities = fetch_collection_activities(collection)

        if stats:
            message += (
                f"\n**{collection}**\n"
                f"- Floor Price: {stats['floor_price']:.2f} SOL\n"
                f"- Volume: {stats['volume_all_time']:.2f} SOL\n"
                f"- Listed Count: {stats['listed_count']}\n"
            )

        if activities:
            message += "**Recent Activities:**\n"
            for activity in activities[:3]:
                tx_type = activity.get("type", "Unknown")
                price = activity.get("price", 0) / 1e9
                message += f"- Type: {tx_type}, Price: {price:.2f} SOL\n"

    await channel.send(message)

# Existing bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Add commands here
@bot.command()
async def help(ctx):
    """Displays a list of available commands."""
    help_message = """
    **Available Commands:**
    - `!help`: Shows this help message.
    - `!ping`: Checks if the bot is online.
    - `!top_collections`: Displays top NFT collections.
    - `!floor_price <collection>`: Displays the floor price of a specific collection.
    - `!stats`: Displays general statistics about the NFT market.
    """
    await ctx.send(help_message)

@bot.command()
async def ping(ctx):
    """Checks if the bot is online."""
    await ctx.send("Pong! 🏓 Bot is online and responsive!")

@bot.command()
async def floor_price(ctx, collection: str):
    """Fetches the floor price of a specific collection."""
    try:
        url = f"https://api-mainnet.magiceden.dev/v2/collections/{collection}/stats"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        floor_price = data.get("floorPrice", 0) / 1e9  # Convert from lamports to SOL
        await ctx.send(f"The floor price for {collection} is {floor_price:.2f} SOL.")
    except Exception as e:
        await ctx.send(f"Error fetching floor price for {collection}: {e}")

@bot.command()
async def stats(ctx):
    """Displays general NFT market statistics."""
    stats_message = """
    **NFT Market Statistics:**
    - Total Volume: 500,000 SOL
    - Top Blockchain: Solana
    - Active Collections: 1,200
    """
    await ctx.send(stats_message)


daily_update.start()
bot.run(TOKEN)

