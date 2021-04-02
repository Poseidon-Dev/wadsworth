import discord, os
from discord.ext import commands

from core.shared.utils import pretty_ping
import core.config

class AssetCommands(commands.Cog, name='asset_commands'):

    def __init__(self, bot):
        self.bot = bot
        if core.config.TESTING:
            self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        else:
            self.channel = self.bot.get_channel(core.config.WADSWORTH_CHANNEL)
        self.ping_channel = self.channel

    @commands.command(name='assets-ping', aliases=['-ap'])
    async def assets_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Assets' module
        """
        embed = pretty_ping(ctx, name=self.__class__.__name__)
        await self.ping_channel.send(embed=embed)