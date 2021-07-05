import discord
from discord.ext import commands, tasks
import smtplib, ssl
from email.message import EmailMessage

import core.config

from .models import OfficeTable
from apps.office.email import OfficeEmail
from apps.office.utils import pretty_keys
from core.shared.utils import send_email

class OfficeTasks(commands.Cog, OfficeTable, name='office_tasks'):

    def __init__(self, bot):
        OfficeTable.__init__(self)
        self.bot = bot
        self.check_for_key_count.start()
        self.check_for_new_keys.start()
        self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)

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



