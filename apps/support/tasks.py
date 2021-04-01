import discord
from discord.ext import commands, tasks

import core.config

from .migrations import JitBitTickets, JitBitTicketComments
from core.shared.utils import pretty_ping

class SupportTasks(commands.Cog, name='support_tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.check_for_desk_changes.start()
        self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        self.ping_channel = self.bot.get_channel(core.config.WADSWORTH_CHANNEL)
        

    @commands.command(name='task-ping', aliases=['tp'])
    async def task_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Task' module
        """
        embed = pretty_ping(ctx, name=self.__class__.__name__)
        await self.ping_channel.send(embed=embed)


    @tasks.loop(seconds=10.0)
    async def check_for_desk_changes(self):
        try:
            ticket = JitBitTickets().check_ticket_differences()
            if ticket:
                JitBitTicketComments().push_comment(ticket)
        except Exception as e:
            print(e)