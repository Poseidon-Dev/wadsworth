from discord.ext import commands, tasks

import core.config
from apps.emailtest.email import TestEmail
from apps.emailtest.utils import pretty_emailtest

class EmailtestTasks(commands.Cog, name='emailtest_tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.emailtest_task.start()
        self.channel = self.bot.get_channel(core.config.EMAIL_CHANNEL)

    @tasks.loop(seconds=5.0)
    async def emailtest_task(self):
        email_from = TestEmail().gather_email()
        if email_from:
            await self.channel.send(embed=pretty_emailtest(email_from))

