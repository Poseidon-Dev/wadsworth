import discord

def ad_user_to_list(account):
    for act in account:
        act = str(act).split(',')[:3]
        act[0] = act[0].replace("<ADUser '", '')
        return act

def pretty_ad_user(account):
    account = ad_user_to_list(account)
    name = account[0].replace('CN=','')
    embed = discord.Embed(
        title=f'{name}'
    )
    embed.add_field(
        name=f'Info',
        value=f"""
        > Type : {account[1]}\n> 
        > DivisionOU : {account[2]}\n
        """,
        inline=False)
    return embed
    