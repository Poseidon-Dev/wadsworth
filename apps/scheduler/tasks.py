import discord
from discord.ext import commands, tasks

import core.config

class SchedulerTasks(commands.Cog, name='scheduler_tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.scheduler_task.start()
        self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)

    @tasks.loop(hours=4.0)
    async def scheduler_task(self):
        return True

