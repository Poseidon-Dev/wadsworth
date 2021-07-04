import discord 

from apps.base.models import Database
from apps.base.queries import Query

def pretty_employee(ctx, employee):
    """
    Returns an embed for an employee for a prettier discord format
    """
    name = f'{employee[1].capitalize()} {employee[2][:1].capitalize()} {employee[4].capitalize()}'
    division = Query('ee_divisions').filter(val=employee[6]).query()
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
        title=f'**{name}**' + '\u2800' * (35 - len(name)),
        color=0x03f8fc,
        timestamp=ctx.message.created_at)
    for employee in employees:
        if employee[7] == 'I':
            status = ' - TERMED'
        else:
            status = ''
        name = f'{employee[1].capitalize()} {employee[2][:1].capitalize()} {employee[4].capitalize()}'
        division = Query('ee_divisions').filter(val=employee[6]).query()
        embed.add_field(
        name=f'{name}' + status + '\n' ,
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
        division = Query('ee_divisions').filter(val=record[6]).query()
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
        
def pretty_property(property):
    from apps.erp.models import EmployeeTable
    prop = property_dict.get(property[3])[1]
    name = f'{EmployeeTable().filter(val=property[1]).query()[0][1].capitalize()} | {prop.capitalize()}'
    embed = discord.Embed(
        title=f'**{name}**' + '\u2800' * (35 - len(name)),
        color=colors_dict.get(prop.lower())
        )
    embed.add_field(
        name='Control',
        value=f'{property[2]}',
        inline=False
    )
    embed.add_field(
        name='Description',
        value=property[4],
        inline=False,
    )
    return embed

def clean_name(name):
    name = name.replace("'", '')
    return name

property_dict = {
    2: ['<:iphone:860220718440251454>', 'iphone'],
    4: ['<:laptop:860213753312575519>', 'laptop'],
    5: ['<:ipad:860220923827585074>', 'ipad'],
    9: ['<:mail:860220741966233630>', 'mail'],
    10: ['<:cards:860220653654376459>', 'cards'],
    70: ['<:docuware:860216636120629298>', 'docuware'],
    75: ['<:concur:860220678748635177>', 'concur']
}

property_emoji_names = [val[1] for k, val in property_dict.items()]

colors_dict = {
    'iphone': 0x00dc9e,
    'laptop': 0x00a3ec,
    'ipad': 0xf400ed,
    'mail': 0xff0909,
    'cards': 0x29e629,
    'docuware': 0x404dff,
    'concur': 0xfdb400,
}