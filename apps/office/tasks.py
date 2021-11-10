import discord
from discord.ext import commands, tasks
import smtplib, ssl
from email.message import EmailMessage
from pickle import loads

import core.config

from .models import OfficeTable
from apps.office.email import OfficeEmail
from apps.office.utils import pretty_keys
from core.shared.utils import send_email
from apps.base import Query

class OfficeTasks(commands.Cog, OfficeTable, name='office_tasks'):

    def __init__(self, bot):
        OfficeTable.__init__(self)
        self.bot = bot
        # self.check_for_key_count.start()
        # self.check_for_new_keys.start()
        self.fetch_keys.start()
        self.channel = self.bot.get_channel(core.config.OFFICE_CHANNEL)

    @tasks.loop(hours=5.0)
    async def check_for_key_count(self):
        count = self.count_available()
        if count <= 3:
            subject = 'Office Keys'
            message = f'There are {count} available keys remaining'
            try:
                send_email(subject, message)
            except Exception as e:
                print(e)
        else:
            print(f'{count} keys remaining')

    @tasks.loop(seconds=60.0)
    async def check_for_new_keys(self):
        key = OfficeEmail().gather_keys()
        if key:
            try: 
                response = self.insert([('office_keys', key), ('available', 1)])
                await self.channel.send(f'I have added key {key} with the others if it didn not already exist') 
            except Exception as e:
                await self.channel.send('That key already exist')

    @tasks.loop(seconds=5.0)
    async def fetch_keys(self):
        office_key_email = Query('email_table').filter('local_read', '0').filter_like('recipient', 'aplbot').filter_like('subject', 'fwd: your digital download instructions').query()
        if office_key_email:
            for e in office_key_email:
                body = loads(e[1]).text.split()
                for word in body:
                    if word.lower() == 'code:':
                        idx = body.index(word) + 1
                        key = body[idx]
                        try: 
                            self.insert([('office_keys', key), ('available', 1)])
                            await self.channel.send(f'A new key, starting: {key[0:4]},  has entered our pipeline, I have added it with the others if it did not already exists')
                            Query('email_table').update_by_key(e[0], [('local_read', 1)])
                        except Exception as e:
                            await self.channel.send('That key already exist')



