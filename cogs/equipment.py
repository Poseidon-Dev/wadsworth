import discord, os, sys
from discord.ext import commands

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

from data import EquipmentsTable

class EquipmentsCog(commands.Cog, EquipmentsTable, name='cog-name'):

    def __init__(self, bot):
        super(EquipmentsCog, self).__init__()
        self.bot = bot
        self.channel = self.bot.get_channel(config.BOT_CHANNEL)


    # Commands
    @commands.command(name='equipment-ping')
    async def equipments_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Equipments' module
        """
        await ctx.send('Equipments Online')

def setup(bot):
    bot.add_cog(EquipmentsCog(bot))
