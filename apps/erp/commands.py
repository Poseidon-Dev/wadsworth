import discord, os
from discord.ext import commands

from core.shared.utils import pretty_ping
from core.shared.messages import property_dict
import core.config
from .utils import pretty_employee, pretty_employees
from .models import EmployeeTable, EmployeePropertyTable

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
    async def employee_records(self, ctx, argument, param1, param2=None):
        """
        [FILTER] [PARAM1] [PARAM2]
        \u2800\u2800Returns employee records based on filter
        \u2800\u2800(-id) : Looks up employee based on Employee ID
        \u2800\u2800(-f) : Looks up employees with first name like [PARAM1] (Active Status)
        \u2800\u2800(-l) : Looks up employees with last name like [PARAM1] (Active Status)
        \u2800\u2800(-fl) : Looks up employees with first name like [PARAM1] and last name like [PARAM2] (Active Status)
        """
        # Argument ID
        if argument in ['id', '-id']:
            if len(param1) != 5:
                await ctx.send('That is not a valid employee number')
            else:
                employees = EmployeeTable().filter('id', param1).query()
                await self.employee_out(ctx, employees)

        # Argument First Name
        if argument in ['f', '-f', 'first', '-first']:
            if len(param1) <= 2:
                await ctx.send('Thats too broad of a search, please be more specific')
            else:
                employees = EmployeeTable().filter_like('first', param1.upper()).query()
                await self.employee_out(ctx, employees)

        # Argument Last Name
        if argument in ['l', '-l', 'last', '-last']:
            if len(param1) <= 2:
                await ctx.send('Thats too broad of a search, please be more specific')
            else:
                employees = EmployeeTable().filter_like('last', param1.upper()).query()
                await self.employee_out(ctx, employees)


        # Argument First and Last Name
        if argument in ['fl', '-fl', 'firstlast', '-firstlast']:
            if len(param1) + len(param2) <= 4:
                await ctx.send('Thats too broad of a search, please be more specific')
            else:
                employees = EmployeeTable().filter_like('first', param1.upper()).filter_like('last', param2.upper()).query()
                await self.employee_out(ctx, employees)


    async def employee_out(self, ctx, employees):
        try:
            msg = await ctx.send(embed=pretty_employees(ctx, employees))
            for emoji in self.employee_property_to_emoji(employees):
                await msg.add_reaction(emoji)
        except Exception as e:
            await ctx.send(f'There was an error with your request')

    def employee_property(self, employee):
        employee_property = EmployeePropertyTable().filter('employeeid', employee[0][0]).query()
        property_type = [prop[3] for prop in employee_property]
        return sorted(list(set(property_type)))


    def employee_property_to_emoji(self, employees):
        emojis = [property_dict.get(prop) for prop in self.employee_property(employees)]
        return emojis

    
            

