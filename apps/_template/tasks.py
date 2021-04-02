import discord
from discord.ext import commands, tasks

import core.config

class TemplateTasks(commands.Cog, name='template_tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.template_task.start()
        self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)

    @tasks.loop(hours=4.0)
    async def template_task(self):
        return True

