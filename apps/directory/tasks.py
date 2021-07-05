from discord.ext import commands, tasks

import core.config

class DirectoryTasks(commands.Cog, name='directory_tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.directory_task.start()
        self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)

    @tasks.loop(hours=4.0)
    async def directory_task(self):
        return True

