import discord, os
from discord.ext import commands

from core.shared.utils import pretty_ping
import core.config
from .utils import pretty_employee
from .models import EmployeeTable

class EmployeeCommands(commands.Cog, EmployeeTable, name='employee_commands'):

    def __init__(self, bot):
        EmployeeTable.__init__(self)
        self.bot = bot
        self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        self.ping_channel = self.channel

    @commands.command(name='employee-ping', aliases=['-ep'])
    async def employee_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Employee' module
        """
        embed = pretty_ping(ctx, name=self.__class__.__name__)
        await self.channel.send(embed=embed)

    @commands.command(name='whois')
    async def employee_records(self, ctx, argument, key):
        """
        [FILTER] [ARG]
        \u2800\u2800Returns employee records based on filter
        \u2800\u2800(-id) : Looks up employee based on Employee ID
        """
        if argument in ['id',]:
            employee = self.select_by_id(int(key), self.table)
            await ctx.send(embed=pretty_employee(ctx, employee[0]))
            # await ctx.send(embed=pretty_assets(ctx, key))