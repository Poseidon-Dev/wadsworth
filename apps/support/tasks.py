import discord
import re
from discord.ext import commands, tasks

import core.config

from .migrations import JitBitTickets
from apps.base.queries import Query
from apps.support.email import SupportEmail
from apps.support.utils import pretty_ticket, support_dict
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


    @tasks.loop(seconds=5.0)
    async def check_tickets(self):
        support_email = Query('email_table').filter('local_read', '0').filter_like('sender', 'support').filter_like('subject', 'new ticket submitted').query()
        if support_email:
            for e in support_email:
                ticket = re.findall('\d{8}', e[2])[0]
                Query('email_table').update_by_key(e[0], [('local_read', 1)])
                try:
                    pwd_rtn = ''
                    ticket_detail = JitBitTickets().pull_ticket(str(ticket))
                    if ticket_detail.get("CategoryID") == 467249:
                        employee_id = re.findall('\d+', ticket_detail.get("Subject"))
                        email_pwd = EmployeePropertyTable().filter('employeeid', employee_id[0]).filter('property_type', 9).query()
                        if email_pwd:
                            for pwd in email_pwd:
                                email_pwd_print = f'Account: {pwd[4]}\nPassword: {pwd[2]}\n\n'
                                pwd_rtn += email_pwd_print
                    msg = await self.channel.send(embed=pretty_ticket(ticket_detail))
                    if pwd_rtn:
                        for k, emoji in support_dict.items():
                            await msg.add_reaction(emoji)
                except Exception as e:
                    print(e)

        # if test_ping_email:
        #     for e in test_ping_email:
        #         Query('email_table').update_by_key(e[0], [('local_read', 1)])
        #         await self.channel.send(embed=pretty_emailtest(loads(e[1])))

        # tickets = SupportEmail().gather_tickets()
        # for ticket_id in tickets:
        #     try:
        #         pwd_rtn = ''
        #         ticket_detail = JitBitTickets().pull_ticket(str(ticket_id[0]))
        #         if ticket_detail.get("CategoryID") == 467249:
        #             employee_id = re.findall('\d+', ticket_detail.get("Subject"))
        #             email_pwd = EmployeePropertyTable().filter('employeeid', employee_id[0]).filter('property_type', 9).query()
        #             if email_pwd:
        #                 for pwd in email_pwd:
        #                     email_pwd_print = f'Account: {pwd[4]}\nPassword: {pwd[2]}\n\n'
        #                     pwd_rtn += email_pwd_print
        #         msg = await self.channel.send(embed=pretty_ticket(ticket_detail))
        #         if pwd_rtn:
        #             for k, emoji in support_dict.items():
        #                 await msg.add_reaction(emoji)
        #     except Exception as e:
        #         print(e)

