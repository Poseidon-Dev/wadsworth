import discord, os, sys
from discord.ext import commands

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

class NewCog(commands.Cog, name='cog-name'):

    def __init__(self, bot):
        self.bot = bot
        self.channel = self.bot.get_channel(config.BOT_CHANNEL)


    # Commands
    @commands.command(name='new-ping')
    async def new_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'New' module
        """
        await ctx.send('New Online')

def setup(bot):
    bot.add_cog(NewCog(bot))
