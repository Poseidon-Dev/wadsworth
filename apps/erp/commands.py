import discord, os
from discord.ext import commands

from core.shared.utils import pretty_ping
import core.config

class EmployeeCommands(commands.Cog, name='Employee'):

    def __init__(self, bot):
        self.bot = bot
        self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        self.ping_channel = self.channel


    # Commands
    @commands.command(name='employee-ping', aliases=['-ep'])
    async def censor_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Employee' module
        """
        embed = pretty_ping(ctx, name=self.__class__.__name__)
        await self.channel.send(embed=embed)