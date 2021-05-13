import discord
from datetime import date
from discord.ext import commands, tasks

import core.config

from .utils import pretty_terms
from .models import EmployeeLogger, Messages
from .migrations import ErpApiConn

class EmployeeTasks(commands.Cog, name='employee_tasks'):

    def __init__(self, bot):
        self.bot = bot
        # self.check_for_employee_changes.start()
        self.updated_records.start()
        self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)

    # @tasks.loop(hours=4.0)
    # async def check_for_employee_changes(self):
    #     try:
    #         ErpApi().insert_employees()
    #         print('erp update complete')
    #     except Exception as e:
    #         print(e)

    @tasks.loop(seconds=5.0)
    async def updated_records(self):
        msg = Messages()
        today = str(date.today())
        records = self.check_data(today)
        try:
            message_id = msg.filter('date', today).select_first().query()[0][0]
            print(message_id)
            message = await self.channel.fetch_message(message_id)
            await message.edit(content=records)
        except:
            message = await self.channel.send(content=records)
            msg.insert([('id', message.id), ('date', today)])
            print('made another')

    def check_data(self, today):
        conn = EmployeeLogger()
        data = conn.changes()
        if data:
            print('data changes... checking...')
            cols = ('id, first, middle1, middle2, last, security, division, status, date')
            for line in data:
                new_line = line + (today, )
                conn.insert_many(cols, new_line)
                conn.upsert_employees(line)
        else:
            print('no data')
        return conn.filter('date', today).query()

                


