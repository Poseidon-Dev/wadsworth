import discord
from discord.ext import commands, tasks

import core.config

class ComdataTasks(commands.Cog, name='comdata_tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.comdata_task.start()
        self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)

    @tasks.loop(hours=4.0)
    async def comdata_task(self):
        return True

