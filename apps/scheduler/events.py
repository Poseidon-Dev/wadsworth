import discord, os, platform, asyncio
from discord.ext import commands

import core.config

class SchedulerEvents(commands.Cog, name='scheduler_events'):

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
        return True

    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload):
    #     if payload.emoji.id in reaction_list:
    #         print('Hello')

    # check the message database for a scheulde, if the message that received a reaction is within the database and the reaction is within parameters
    # then process changes to the scheduled task


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        print('Goodbye')