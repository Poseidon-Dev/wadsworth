import discord
from datetime import datetime

def pretty_emailtest(email):
    format = '%a, %b %d, %Y | %I:%M:%S %p'
    platform = email.headers['x-mailer'][0]
    embed = discord.Embed(title='Recevied Email Test')
    embed.add_field(name='Address', value=str(email.from_), inline=False)
    if platform:
        embed.add_field(name='Platform', value=str(platform), inline=False)
    embed.add_field(name='Timestamp', value=str(datetime.strftime(email.date, format)), inline=False)
    return embed
    