import discord
from discord.ext import commands, tasks

import core.config

from .migrations import JitBitTickets
from apps.support.email import SupportEmail
from apps.support.utils import pretty_ticket

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
                await self.channel.send(embed=pretty_ticket(ticket_detail))
            except Exception as e:
                print(e)