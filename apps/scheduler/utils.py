import discord
from datetime import datetime

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
    