import discord, os
from discord.ext import commands

from core.shared.utils import pretty_ping
import core.config

class SchedulerCommands(commands.Cog, name='scheduler_commands'):

    def __init__(self, bot):
        self.bot = bot
        if core.config.TESTING:
            self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        else:
            self.channel = self.bot.get_channel(core.config.WADSWORTH_CHANNEL)
        self.ping_channel = self.channel

    # Commands
    @commands.command(name='scheduler-ping', aliases=['-tp'])
    async def scheduler_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Scheduler' module
        """
        embed = pretty_ping(ctx, name=self.__class__.__name__)
        await self.ping_channel.send(embed=embed)