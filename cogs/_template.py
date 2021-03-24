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
    @commands.command(name='office-ping')
    async def office_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Office' module
        """
        embed = Pretty().pretty_ping(ctx, name=self.__class__.__name__)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(NewCog(bot))
