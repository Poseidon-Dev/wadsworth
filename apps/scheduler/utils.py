import discord
from datetime import datetime

from apps.scheduler.models import SchedulerUserTable

def pretty_scheduler(ctx, data: list):
    name = 'Employee Search Results'
    embed = discord.Embed(
        title=f'**{data[0].upper()}**',
        description=data[1].capitalize(),
        color=0x03f8fc)
    date_value = data[2]
    date_format = "%a - %B %d, %Y @ %I:%M %p"
    embed.add_field(name='Time', value=f'{date_value.strftime(date_format)}', inline=False)
    users = [f'{i}' for i in 'phrase']
    embed.add_field(
        name=f'Accepted (0/3)' + '\u2800' *5 +'\n',
        value='\n'.join(users),
        inline=True)
    embed.add_field(
        name=f'Declined (0/3)' + '\u2800' *5 +'\n',
        value='\n'.join(users),
        inline=True)
    embed.add_field(
        name=f'Tenative (0/3)' + '\u2800' *5 +'\n',
        value='\n'.join(users),
        inline=True)
    footer = True
    if footer:
        footer_txt = f'Created by Johnny • Does not repeat'
    embed.set_footer(text=footer_txt)
    return embed

def pretty_scheduler_from_db(data):
    name = 'Employee Search Results'
    embed = discord.Embed(
        title=f'**{data[4].upper()}**',
        description=data[5].capitalize(),
        color=0x03f8fc)
    date_value = datetime.strptime(data[6], '%Y-%m-%d %H:%M:%S')
    date_format = "%a - %B %d, %Y @ %I:%M %p"
    embed.add_field(name='Time', value=f'{date_value.strftime(date_format)}', inline=False)
    users = SchedulerUserTable().filter('schedule_id', data[0]).query()
    accepted = [user[2] for user in users if user[3] == 1]
    declined = [user[2] for user in users if user[3] == 0]
    tenative = [user[2] for user in users if user[3] == 2]
    count = len(users)
    if accepted:
        embed.add_field(
            name=f'Accepted ({len(accepted)}/{count})' + '\u2800' *5 +'\n',
            value='\n'.join(accepted),
            inline=True)
    if declined:
        embed.add_field(
            name=f'Declined ({len(declined)}/{count})' + '\u2800' *5 +'\n',
            value='\n'.join(declined),
            inline=True)
    if tenative:
        embed.add_field(
            name=f'Tenative ({len(tenative)}/{count})' + '\u2800' *5 +'\n',
            value='\n'.join(tenative),
            inline=True)
    footer = True
    if footer:
        footer_txt = f'Created by Johnny • Does not repeat'
    embed.set_footer(text=footer_txt)
    return embed
    