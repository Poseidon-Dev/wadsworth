import discord, os, sys
from discord.ext import commands

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

class CensorCog(commands.Cog, name='Censor-Cog'):

    def __init__(self, bot):
        self.bot = bot
        self.channel = self.bot.get_channel(config.BOT_CHANNEL)
        self.ping_channel = self.bot.get_channel(config.WADSWORTH_CHANNEL)

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        for word in message.content.split():
            if word.lower() in config.SWEAR_LIST:
                await message.delete()
                await message.channel.send("Please don't speak that way in this server.")


    # Commands
    @commands.command(name='censor-ping')
    async def office_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Censor' module
        """
        embed = Pretty().pretty_ping(ctx, name=self.__class__.__name__)
        await self.ping_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(CensorCog(bot))
