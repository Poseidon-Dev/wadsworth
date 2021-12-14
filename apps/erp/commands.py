import discord, os
from discord.ext import commands

from core.shared.utils import pretty_ping
from apps.erp.models import Employee
import core.config
from .utils import pretty_employee, pretty_employees, property_dict
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


    @commands.command(name='whois', aliases=['-w'])
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

        # Argument First and Last Name
        if argument in ['s']:
            if len(param1) + len(param2) <= 4:
                await ctx.send('Thats too broad of a search, please be more specific')
            else:
                employees = EmployeeTable().filter_like('first', param1.upper()).filter_like('last', param2.upper()).query()
                await ctx.send(embed=pretty_employees(ctx, employees))
                for employee in employees:
                    phones = EmployeePropertyTable().filter('employeeid', employee[0]).filter('property_type', 2).query()
                    for phone in phones:
                        await ctx.send(f'{phone[2]} {phone[4]}: ')
                    emails = EmployeePropertyTable().filter('employeeid', employee[0]).filter('property_type', 9).query()
                    for email in emails:
                        await ctx.send(f'{email[4]}')
                

    async def employee_out(self, ctx, employees):
        try:
            for employee in employees:
                employee = Employee(record=employee)
                msg = await ctx.send(embed=pretty_employee(ctx, employee))
                for emoji in self.employee_property_to_emoji(employee.company_property):
                    await msg.add_reaction(emoji[0])
        except Exception as e:
            await ctx.send(f'There was an error with your request: {e}')


    def employee_property_type(self, employee):
        employee_property = EmployeePropertyTable().filter('employeeid', employee[0][0]).query()
        property_type = [prop[3] for prop in employee_property]
        return sorted(list(set(property_type)))


    def employee_property_to_emoji(self, company_property):
        return [property_dict.get(prop[3]) for prop in company_property]

