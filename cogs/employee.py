import discord, os, sys
from discord.ext import commands

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

from data import EmployeeTable
from utils import Pretty

class EmployeeCog(commands.Cog, EmployeeTable, name='employee'):

    def __init__(self, bot):
        EmployeeTable.__init__(self)
        self.bot = bot
        self.channel = self.bot.get_channel(config.BOT_CHANNEL)


    # Commands
    @commands.command(name='emp-ping')
    async def office_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Employee' module
        """
        embed = Pretty().pretty_ping(ctx, name=self.__class__.__name__)
        await ctx.send(embed=embed)

    @commands.command(name='whois')
    async def employee_records(self, ctx, argument, key):
        if argument in ['id',]:
            employee = self.select_row_by_key(self.table, int(key))
            await ctx.send(embed=Pretty().pretty_employee(ctx, employee[0]))

def setup(bot):
    bot.add_cog(EmployeeCog(bot))
