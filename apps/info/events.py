import discord, os, platform, asyncio
from discord.ext import commands

import core.config

class InfoEvents(commands.Cog, name='info_events'):

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
        if '/?' in message.content and message.author.id == 816733794878750793 :
            await message.channel.send('Go jump off a fuking cliff, brion')
