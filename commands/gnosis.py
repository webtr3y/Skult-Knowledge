from discord.ext import commands
import os
from gnosis import Gnosis  # Assuming Eliza's framework is properly installed and accessible

class GnosisCommands(commands.Cog):
    """Commands for interacting with Gnosis AI."""

    def __init__(self, bot):
        self.bot = bot
        self.gnosis = Eliza()
        self.gnosis.load('./eliza/rules.dat')  # Load conversation rules

    @commands.command(name="chat")
    async def chat(self, ctx, *, user_input: str):
        """Chat with Gnosis."""
        response = self.gnosis.respond(user_input)
        await ctx.send(f"**Gnosis:** {response}")

    @commands.command(name="crypto_help")
    async def crypto_help(self, ctx, *, question: str):
        """Ask Gnosis about crypto-related topics."""
        if "price" in question.lower():
            await ctx.send("Gnosis: Use `!crypto_stats` to get the latest price information.")
        else:
            response = self.gnosis.respond(question)
            await ctx.send(f"**Gnosis:** {response}")

    @commands.command(name="nft_advice")
    async def nft_advice(self, ctx, *, question: str):
        """Ask Gnosis about NFT-related topics."""
        response = self.gnosis.respond(f"NFTs {question}")
        await ctx.send(f"**Gnosis:** {response}")

    @commands.command(name="trade_tips")
    async def trade_tips(self, ctx):
        """Ask Gnosis for general trading advice."""
        tips = [
            "Diversify your portfolio to minimize risk.",
            "Track whale wallets for potential trends.",
            "Keep an eye on news affecting the broader crypto market.",
            "Use NFT analytics to understand undervalued assets."
        ]
        await ctx.send(f"**Gnosis:** Here are some trade tips:\n" + "\n".join(tips))

    @commands.command(name="trend_analysis")
    async def trend_analysis(self, ctx, *, keyword: str):
        """Ask Gnosis to analyze a trend."""
        response = self.gnosis.respond(f"Analyze trend: {keyword}")
        await ctx.send(f"**Gnosis:** {response}")

    @commands.command(name="cycle_explanation")
    async def cycle_explanation(self, ctx):
        """Gnosis explains market cycles."""
        response = (
            "Market cycles consist of accumulation, markup, distribution, and markdown. "
            "Understanding where the market is in its cycle can inform your strategy."
        )
        await ctx.send(f"**Gnosis:** {response}")

    @commands.command(name="find_opportunities")
    async def find_opportunities(self, ctx, market: str):
        """Ask Gnosis to find trading opportunities in a specific market."""
        opportunities = [
            f"Look for undervalued NFTs in {market}.",
            f"Monitor recent activities on {market} to identify trends.",
            "Find early entries into new NFT collections or tokens."
        ]
        await ctx.send(f"**Gnosis:** Opportunities in {market}:\n" + "\n".join(opportunities))

    @commands.Cog.listener()
    async def on_message(self, message):
        """Allow Gnosis to respond freely in chat."""
        if message.author == self.bot.user:
            return

        if "gnosis" in message.content.lower():
            user_input = message.content.lower().replace("gnosis", "").strip()
            if user_input:
                response = self.gnosis.respond(user_input)
                await message.channel.send(f"**Gnosis:** {response}")

from discord.ext import commands

class Tips(commands.Cog):
    """Commands for providing trading tips."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tips(self, ctx):
        """Provide trading tips."""
        await ctx.send("Here’s a tip: Always set stop-loss orders!")

def setup(bot):
    bot.add_cog(Tips(bot))


import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

class GnosisAI(commands.Cog):
    """AI-Driven Assistant Commands for Gnosis."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ask_gnosis(self, ctx, *, question: str):
        """Ask Gnosis a question and receive an AI-driven response."""
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Act as a trading assistant specializing in meme coins and NFTs. {question}",
                max_tokens=150,
                temperature=0.7
            )
            answer = response.choices[0].text.strip()
            await ctx.send(f"Gnosis: {answer}")
        except Exception as e:
            await ctx.send(f"Error: {e}")

def setup(bot):
    bot.add_cog(GnosisAI(bot))



@bot.tree.command(name="gnosis_query", description="Ask Gnosis a trading question!")
async def gnosis_query(interaction: discord.Interaction, question: str):
    response = gnosis_agent.process_query(question)  # Use your AI processing logic
    await interaction.response.send_message(response)

@bot.tree.command(name="gnosis_tips", description="Get AI-driven trading tips!")
async def gnosis_tips(interaction: discord.Interaction):
    tips = gnosis_agent.get_trading_tips()  # Example: AI-generated trading advice
    await interaction.response.send_message(tips)



# Function to add the cog to the bot
def setup(bot):
    bot.add_cog(GnosisCommands(bot))
