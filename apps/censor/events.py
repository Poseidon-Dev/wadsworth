import discord, os, platform, asyncio
from discord.ext import commands

import core.config

class CensorEvents(commands.Cog, name='censor_events'):

    def __init__(self, bot):
        self.bot = bot
        if core.config.TESTING:
            self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        else:
            self.channel = self.bot.get_channel(core.config.WADSWORTH_CHANNEL)
        self.ping_channel = self.channel

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        for word in message.content.split():
            if word.lower() in core.config.SWEAR_LIST:
                await message.delete()
                await message.channel.send("Please don't speak that way in this server.")