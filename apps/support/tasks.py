import discord
import re
from discord.ext import commands, tasks

import core.config

from .migrations import JitBitTickets
from apps.support.email import SupportEmail
from apps.support.utils import pretty_ticket
from apps.erp.models import EmployeePropertyTable

from core.shared.utils import pretty_ping


class SupportTasks(commands.Cog, name='support_tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.check_tickets.start()
        self.channel = self.bot.get_channel(core.config.TICKET_CHANNEL)
        self.ping_channel = self.bot.get_channel(core.config.WADSWORTH_CHANNEL)
        

    @commands.command(name='task-ping', aliases=['tp'])
    async def task_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Task' module
        """
        embed = pretty_ping(ctx, name=self.__class__.__name__)
        await self.ping_channel.send(embed=embed)


    @tasks.loop(seconds=30)
    async def check_tickets(self):
        tickets = SupportEmail().gather_tickets()
        for ticket_id in tickets:
            try:
                ticket_detail = JitBitTickets().pull_ticket(str(ticket_id[0]))
                if ticket_detail.get("CategoryID") == 467249:
                    employee_id = re.findall('\d+', ticket_detail.get("Subject"))
                    email_pwd = EmployeePropertyTable().filter('employeeid', employee_id[0]).filter('property_type', 9).query()
                    if email_pwd:
                        pwd_rtn = ''
                        for pwd in email_pwd:
                            email_pwd_print = f'Account: {pwd[4]}\nPassword: {pwd[2]}\n\n'
                            pwd_rtn += email_pwd_print
                        JitBitTickets().post_ticket_comment(str(ticket_id[0]), pwd_rtn)
                        # await self.channel.send(embed=pretty_ticket(ticket_detail))
            except Exception as e:
                print(e)