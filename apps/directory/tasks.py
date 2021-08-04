from discord.ext import commands, tasks

import core.config
from apps.base import Query
from apps.erp.models import EmployeeTable
from apps.directory.queries import ad_query
from apps.directory.utils import email_to_ad, pretty_ad_user, directory_emojis, ad_user_to_list
class DirectoryTasks(commands.Cog, name='directory_tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.directory_task.start()
        self.channel = self.bot.get_channel(core.config.LOA_CHANNEL)

    @tasks.loop(seconds=5.0)
    async def directory_task(self):
        loa_email = Query('email_table').filter('local_read', '0').filter_like('recipient', 'itloa').query()
        loa_list = email_to_ad(loa_email)
        for email in loa_list:
            employee = self.email_to_employee(email)
            Query('email_table').update_by_key(email['key'], [('local_read', 1)])
            if employee:
                ad_acts = self.employee_ad_search(employee)
                if len(ad_acts) == 1:
                    msg = await self.channel.send(embed=pretty_ad_user(ad_acts, employee['command']))
                    emoji = directory_emojis[employee['command'].lower()]
                    await msg.add_reaction(emoji)
                elif len(ad_acts) > 1:
                    await self.channel.send('Multiple accounts were found, please select from the below')
                    for account in ad_acts:
                        msg = await self.channel.send(embed=pretty_ad_user(account, employee['command']))
                        emoji = directory_emojis[employee['command'].lower()]
                        await msg.add_reaction(emoji)
                elif not ad_acts:
                    msg = ''
                    await self.channel.send(f'No AD account for {employee["first"].capitalize()} {employee["last"].capitalize()} found')
            else:
                await self.channel.send(f'Employee can not be found (Incorrect Email Format?):\nEEID Provided: {email["id"]}\nCommand Provided: {email["command"]}')
     
    @staticmethod
    def email_to_employee(email):
        if email['id']:
            employee = EmployeeTable().filter('id', email['id'][0]).query()[0]
            employee = {'first': employee[1], 'middle': employee[2], 'last': employee[4], 'command': email['command']}
            return employee

    @staticmethod
    def employee_ad_search(employee):
        accounts = ad_query(employee['first'], employee['last'])
        return accounts
