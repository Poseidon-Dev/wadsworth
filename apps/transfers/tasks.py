import discord
import re
from discord.ext import commands, tasks
from pickle import loads

import core.config
from apps.base import Query
from apps.erp import Employee
from apps.transfers.utils import pretty_transfer

class TransfersTasks(commands.Cog, name='transfers_tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.transfers_task.start()
        self.transfers_check.start()
        self.channel = self.bot.get_channel(core.config.BOT_EMPLOYEE_CHANGES)

    @tasks.loop(hours=4.0)
    async def transfers_task(self):
        return True

    @tasks.loop(seconds=5)
    async def transfers_check(self):
        # email = Query('email_table').filter('recipient', 'transfers').query()
        email = Query('email_table').filter('local_read', '0').filter_like('recipient', 'transfers').query()
        for e in email:
            msg = loads(e[1])
            employee_id = re.findall('\d{5}', msg.text)[0]
            employee = Employee(id=employee_id)
            await self.channel.send(embed=pretty_transfer(employee))
            Query('email_table').update_by_key(msg.uid, [('local_read', 1)])              
