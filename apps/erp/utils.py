import discord 

from apps.base.models import Database
from apps.base.queries import Query

def pretty_employee(ctx, employee):
    """
    Returns an embed for an employee for a prettier discord format
    """
    name = f'{employee[1].capitalize()} {employee[2][:1].capitalize()} {employee[4].capitalize()}'
    division = Query('division_table').filter(val=employee[6]).query()
    # division = Database().select_by_id(table='division_table', key=employee[6])
    embed = discord.Embed(
        title=f'**{name}**',
        color=0x03f8fc,
        timestamp=ctx.message.created_at)
    embed.add_field(
        name=f'{employee[0]}',
        value=f"""
        > Division : {division[0][1]}\n> 
        > Status : {employee[7]}\n> 
        > Security : {employee[5]}\n> 
        """ + '\u2800' * 27,
        inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
    return embed

def pretty_employees(ctx, employees):
    """
    Returns an embed for a list of employees for a prettier discord format
    """
    name = 'Employee Search Results'
    embed = discord.Embed(
        title=f'**{name}**',
        color=0x03f8fc,
        timestamp=ctx.message.created_at)
    for employee in employees:
        name = f'{employee[1].capitalize()} {employee[2][:1].capitalize()} {employee[4].capitalize()}'
        division = Query('division_table').filter(val=employee[6]).query()
        embed.add_field(
        name=f'{name}\n',
        value=f"""
        > ID : {employee[0]}\n> 
        > Division : {division[0][1]}\n> 
        > Security : {employee[5]}\n> 
        """ + '\u2800' * 27,
        inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
    return embed

def pretty_terms(data):
    """
    Returns the currently changes records in HR by date
    """
    from datetime import date
    name = f'Changes | {str(date.today())}'
    embed = discord.Embed(
        title=f'**{name}**',
        color=0x03f8fc,)
    for record in data:
        division = Query('division_table').filter(val=record[6]).query()
        embed.add_field(
            name=f'Employee',
            value=f"""
            > ID : {record[0]}\n> 
            > Name: {record[1].capitalize()} {record[4].capitalize()}\n> 
            > Division: {division[0][1]}\n> 
            > Security: {record[5]}\n> 
            > Changes: {record[11]}\n> 
            """ + '\u2800' * 27,
            inline=False)
    return embed
        

def clean_name(name):
    name = name.replace("'", '')
    return name