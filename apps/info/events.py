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
        if message.content == '/?':
            await message.channel.send('info events')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print('Hello')
        print(payload.__dir__())
        print(payload.event_type)
        print(payload.emoji)
        print(payload.channel_id)
        print(payload.message_id)
        print(payload.member)


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        print('Goodbye')