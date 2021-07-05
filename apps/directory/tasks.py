from discord.ext import commands, tasks

import core.config
from apps.directory.email import DirectoryEmail
from apps.erp.models import EmployeeTable
from apps.directory.queries import ad_query
from apps.directory.utils import pretty_ad_user
class DirectoryTasks(commands.Cog, name='directory_tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.directory_task.start()
        self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)

    @tasks.loop(hours=4.0)
    async def directory_task(self):
        people = DirectoryEmail().gather_employees()
        for emp in people:
            employees = EmployeeTable().filter('id', emp).query()
            if employees:
                print(employees)
                for employee in employees:
                    ad_account = ad_query(employee[1], employee[4])
                    await self.channel.send(embed=pretty_ad_user(ad_account))
                    

