import discord
from datetime import date
from discord.ext import commands, tasks

import core.config
from core.config import log
from core.shared.utils import send_email

from .utils import pretty_terms
from .models import EmployeeTable, EmployeeUpdatesTable, EmployeeLoggerTable, EmployeeDivisionTable, EmployeeMessagesTable
from .migrations import EmployeeMasterMigration, EmployeeUpdatesMigration, EmployeeLoggerMigrations, EmployeeDivisionMigration, EmployeePropertyMigrations

class EmployeeTasks(commands.Cog, name='employee_tasks'):

    def __init__(self, bot):
        self.bot = bot
        # self.updated_records.start()
        self.update_company_property.start()
        # self.send_updates.start()
        self.channel = self.bot.get_channel(core.config.BOT_TERMS_CHANNEL)
        EmployeeMasterMigration().store()
        EmployeeDivisionMigration().insert_divisions()

    @tasks.loop(seconds=600)
    async def update_company_property(self):
        migrations = EmployeePropertyMigrations()
        migrations.refresh()

    @tasks.loop(seconds=5.0)
    async def updated_records(self):
        msg = EmployeeMessagesTable()
        today = str(date.today())
        records = self.check_data(today)
        try:
            message_id = msg.filter('date', today).select_first().query()[0][0]
            message = await self.channel.fetch_message(message_id)
            await message.edit(embed=pretty_terms(records))
        except:
            message = await self.channel.send(embed=pretty_terms(records))
            msg.insert([('id', message.id), ('date', today)])

    @tasks.loop(minutes=5.0)
    async def send_updates(self):
        records = EmployeeLogger().filter('date', str(date.today())).query()
        send_email('Updated Employees', str(records), 'jwhitworth@arizonapipeline.com')

    def check_data(self, today):
        conn = EmployeeLoggerMigrations()
        emp = EmployeeUpdatesMigration()
        emp.refresh()
        data = conn.collect_changes()
        if data:
            cols = conn.column_names_to_string()
            cols_list = cols.split(',')
            for line in data:
                new = line + (today,)
                old = EmployeeTable().filter('id', line[0]).query()[0] + (today,)
                changes = [f'{cols_list[i-1].upper()}: NEW - {new[i-1]} | OLD - {old[i-1]}' for i in range(len(cols_list)) if new[i-1] != old[i-1]]
                changes = (new + (str(changes).strip('[]').replace("'", ''),))
                conn.upsert_logger(changes)
                EmployeeMasterMigration().upsert_records(line)
        data = conn.filter('date', today).query()
        return data

                


