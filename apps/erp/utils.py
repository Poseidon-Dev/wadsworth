import discord 

from apps.base.models import Database

def pretty_employee(ctx, employee):
    """
    Returns an embed for an employee for a prettier discord format
    """
    name = f'{employee[1]} {employee[2][:1]} {employee[4]}'
    division = Database().select_by_id(table='division_table', key=employee[6])
    
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
    embed.set_footer(text=f"Requested by {ctx.message.author}")
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
        name = f'{employee[1]} {employee[2][:1]} {employee[4]}'
        division = Database().select_by_id(table='division_table', key=employee[6])
        embed.add_field(
        name=f'{name}\n',
        value=f"""
        > ID : {employee[0]}\n> 
        > Division : {division[0][1]}\n> 
        > Security : {employee[5]}\n> 
        """ + '\u2800' * 27,
        inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    return embed

def pretty_terms(ctx, data):
    """
    Returns the currently changes records in HR by date
    """
    from datetime import date
    name = f'Changes | {str(date.today())}'
    embed = discord.Embed(
        title=f'**{name}**',
        color=0x03f8fc,
        timestamp=ctx.message.created_at)
    for record in data:
        embed.add_field(
            name=f'Employee',
            value=f"""
            > ID : {record[0]}\n>
            > Name: {record[1].capital()} {record[4].capital()}\n>
            > Division: {record[5]}\n>
            > Status: {record[7]}'
            """ + '\u2800' * 27,
            inline=False)
    return embed
        

def clean_name(name):
    name = name.replace("'", '')
    return name