import discord

def pretty_emailtest(email):
    embed = discord.Embed(
        title='Recevied Email Test'
    )
    embed.add_field(
        name='Address',
        value=str(email[0]),
    )
    return embed
    