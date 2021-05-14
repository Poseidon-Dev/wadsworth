import discord
from datetime import date
from discord.ext import commands, tasks

import core.config

from .utils import pretty_terms
from .models import EmployeeLogger, Messages, EmployeeChangesTable, EmployeeTable
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
            message = await self.channel.fetch_message(message_id)
            await message.edit(embed=pretty_terms(records))
        except:
            message = await self.channel.send(embed=pretty_terms(records))
            msg.insert([('id', message.id), ('date', today)])

    def check_data(self, today):
        conn = EmployeeLogger()
        emp = EmployeeChangesTable()
        emp.db_refresh()
        data = conn.changes()
        if data:
            print('change found')
            cols = ('empid, first, middle1, middle2, last, security, division, status, date, type')
            for line in data:
                new_line = line + (today, 'U')
                old_data = EmployeeTable().filter('id', line[0]).query()[0]
                old_line = old_data + (today, 'H')
                conn.insert_many(cols, new_line)
                conn.insert_many(cols, old_line)
                conn.upsert_employees(line)
        data = conn.filter('date', today).filter('type', 'U').query()
        return data

                


