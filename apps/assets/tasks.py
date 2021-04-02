import discord
from discord.ext import commands, tasks

import core.config

class AssetsTasks(commands.Cog, name='assets_tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.asset_loop.start()
        self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)

    @tasks.loop(seconds=10.0)
    async def asset_loop(self):
        print('Asset loop')
