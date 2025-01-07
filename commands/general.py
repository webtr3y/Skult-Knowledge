
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Shows this help message."""
        await ctx.send("This is the help command!")

    @commands.command(name="ping")
    async def ping(self, ctx):
        """Checks if the bot is online."""
        await ctx.send("Pong! 🏓")

def setup(bot):
    bot.add_cog(General(bot))
