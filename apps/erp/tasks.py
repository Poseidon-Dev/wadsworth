import discord
from datetime import date
from discord.ext import commands, tasks

import core.config
from core.config import log

from .utils import pretty_terms
from .models import EmployeeLogger, Messages, EmployeeChangesTable, EmployeeTable
from .migrations import ErpApiConn

class EmployeeTasks(commands.Cog, name='employee_tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.updated_records.start()
        self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        # EmployeeChangesTable().db_refresh()

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
            log.info('employee record differences found...')
            cols = ('empid, first, middle1, middle2, last, security, division, status, property_type, device_control, device_description, date, log')
            cols_list = ['empid', 'first', 'middle1', 'middle2', 'last', 'security', 'division', 'status', 'property_type', 'device_control', 'device_description', 'date']
            for line in data:
                new = line + (today,)
                old = EmployeeTable().filter('id', line[0]).query()[0] + (today,)
                changes = [f'{cols_list[i].upper()} - New: {new[i]} Old: {old[i]}' for i in range(len(cols_list)) if new[i] != old[i]]
                changes = (new + (str(changes).strip('[]').replace("'", ''),))
                conn.insert_many(cols, changes)
                conn.upsert_employees(line)
        data = conn.filter('date', today).query()
        return data

                


