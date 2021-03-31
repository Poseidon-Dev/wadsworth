import discord, os, platform, asyncio
from discord.ext import commands

import core.config

class TemplateEvents(commands.Cog, name='template_events'):

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
        if message.content == '/?':
            await message.channel.send('template events')