import discord
from discord.ext import commands, tasks

import core.config

from .migrations import ErpApi

class EmployeeTasks(commands.Cog, name='employee_tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.check_for_employee_changes.start()
        self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)

    @tasks.loop(hours=4.0)
    async def check_for_employee_changes(self):
        try:
            ErpApi().insert_employees()
            print('erp update complete')
        except Exception as e:
            print(e)

