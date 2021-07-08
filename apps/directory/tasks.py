from discord.ext import commands, tasks

import core.config
from apps.directory.email import DirectoryEmail
from apps.erp.models import EmployeeTable
from apps.directory.queries import ad_query
from apps.directory.utils import pretty_ad_user, directory_emojis
class DirectoryTasks(commands.Cog, name='directory_tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.directory_task.start()
        self.channel = self.bot.get_channel(core.config.LOA_CHANNEL)

    @tasks.loop(seconds=60.0)
    async def directory_task(self):
        people = DirectoryEmail().gather_loa()
        for emp in people:
            employee = EmployeeTable().filter('id', emp[0]).query()
            if employee:
                employee = employee[0] + (emp[1],)
                ad_accounts = ad_query(employee[1], employee[4])
                if len(ad_accounts) == 1:
                    msg = await self.channel.send(embed=pretty_ad_user(ad_accounts, employee[-1]))
                    emoji = directory_emojis[employee[-1].lower()]
                    await msg.add_reaction(emoji)
                elif len(ad_accounts) > 1:
                    await self.channel.send('Multiple accounts were found, please select from the below')
                    for account in ad_accounts:
                        msg = await self.channel.send(embed=pretty_ad_user(account, employee[-1]))
                        emoji = directory_emojis[employee[-1].lower()]
                        await msg.add_reaction(emoji)
                elif not ad_accounts:
                    await self.channel.send(f'No AD account for {employee[1].capitalize()} {employee[4].capitalize()}')
            else:
                await self.channel.send('Employee does not exist')

                    

