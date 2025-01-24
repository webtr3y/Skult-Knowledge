import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
COINMARKETCAP_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

# Helper Function to Fetch Data
def fetch_crypto_data(limit=10, convert="USD"):
    """Fetch top cryptocurrencies by market cap."""
    try:
        headers = {"X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY}
        params = {
            "start": 1,  # Starting rank
            "limit": limit,  # Number of results
            "convert": convert,  # Conversion currency
        }
        response = requests.get(COINMARKETCAP_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except Exception as e:
        print(f"Error fetching cryptocurrency data: {e}")
        return []

# Cog for Crypto Commands
class CryptoCommands(commands.Cog):
    """Crypto-related commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def crypto_stats(self, ctx):
        """Display top cryptocurrency stats."""
        cryptos = fetch_crypto_data(limit=5)
        if not cryptos:
            await ctx.send("Could not fetch cryptocurrency data.")
            return

        message = "**Top Cryptocurrencies:**\n"
        for crypto in cryptos:
            name = crypto["name"]
            symbol = crypto["symbol"]
            price = crypto["quote"]["USD"]["price"]
            change_24h = crypto["quote"]["USD"]["percent_change_24h"]
            market_cap = crypto["quote"]["USD"]["market_cap"]
            message += (
                f"- {name} ({symbol}):\n"
                f"  - Price: ${price:.2f}\n"
                f"  - 24h Change: {change_24h:+.2f}%\n"
                f"  - Market Cap: ${market_cap:.2f}\n\n"
            )

        await ctx.send(message)

    @commands.command()
    async def crypto_price(self, ctx, symbol: str):
        """Fetch the price of a specific cryptocurrency."""
        cryptos = fetch_crypto_data(limit=100)
        crypto = next((c for c in cryptos if c["symbol"].lower() == symbol.lower()), None)

        if not crypto:
            await ctx.send(f"Cryptocurrency '{symbol}' not found.")
            return

        name = crypto["name"]
        price = crypto["quote"]["USD"]["price"]
        change_24h = crypto["quote"]["USD"]["percent_change_24h"]
        await ctx.send(
            f"**{name} ({symbol.upper()}):**\n"
            f"  - Price: ${price:.2f}\n"
            f"  - 24h Change: {change_24h:+.2f}%"
        )

# Function to add the cog to the bot
def setup(bot):
    bot.add_cog(CryptoCommands(bot))
