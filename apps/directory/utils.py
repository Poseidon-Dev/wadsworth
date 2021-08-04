import discord
import re
from apps.base import Query
from pickle import loads

def email_to_ad(email):
    """
    Subject 10556 / Brion Morris / LOA
    Text 'Command'
    """
    directory_email = Query('email_table').filter('local_read', '0').filter_like('recipient', 'itloa').query()
    loa_list = []
    for e in directory_email:
        ee_id = re.findall('\d{5}', e[2])
        command = loads(e[1]).text.split()[0]
        loa_list.append({'id': ee_id, 'command': command, 'key': e[0]})
    return loa_list

def ad_user_to_list(account):
    account = str(account).split(',')
    account[0] = account[0].replace("[", '')
    account[0] = account[0].replace("<ADUser '", '')
    return account

def pretty_ad_user(account, command):
    account = ad_user_to_list(account)
    name = account[0].replace('CN=','')
    embed = discord.Embed(
        title=f'{name}'
    )
    embed.add_field(
        name=f'{command}',
        value=f"""
        > Division : {account[2].replace('OU=', '')}\n
        """,
        inline=False)
    return embed

directory_emojis = {
    'returning': '<:returning:862824435157696513>',
    'exiting': '<:exiting:862824523527094303>',
}
directory_emojis_list = [k for k, v in directory_emojis.items()]
