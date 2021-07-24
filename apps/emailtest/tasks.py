from apps.base.queries import Query
from discord.ext import commands, tasks

import core.config
from apps.emailtest.utils import pretty_emailtest
from pickle import loads

class EmailtestTasks(commands.Cog, name='emailtest_tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.emailtest_task.start()
        self.channel = self.bot.get_channel(core.config.EMAIL_CHANNEL)

    @tasks.loop(seconds=5.0)
    async def emailtest_task(self):
        test_ping_email = Query('email_table').filter('local_read', '0').filter_like('recipient', 't').query()
        if test_ping_email:
            for e in test_ping_email:
                Query('email_table').update_by_key(e[0], [('local_read', 1)])
                await self.channel.send(embed=pretty_emailtest(loads(e[1])))
