import discord, os
from discord.ext import commands

from core.shared.utils import pretty_ping
import core.config
from .models import TicketTable

class SupportCommands(commands.Cog, TicketTable, name='support_commands'):

    def __init__(self, bot):
        TicketTable.__init__(self)
        self.bot = bot
        if core.config.TESTING:
            self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        else:
            self.channel = self.bot.get_channel(core.config.WADSWORTH_CHANNEL)
        self.ping_channel = self.channel

    # Commands
    @commands.command(name='support-ping', aliases=['-sp'])
    async def support_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Support' module
        """
        embed = pretty_ping(ctx, name=self.__class__.__name__)
        await self.ping_channel.send(embed=embed)


    