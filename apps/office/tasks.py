import discord
from discord.ext import commands, tasks
import smtplib, ssl
from email.message import EmailMessage

import core.config

from .models import OfficeTable
from core.shared.utils import send_email

class OfficeTasks(commands.Cog, OfficeTable, name='office tasks'):

    def __init__(self, bot):
        OfficeTable.__init__(self)
        self.bot = bot
        self.check_for_key_count.start()
        self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)

    @tasks.loop(minutes=5.0)
    async def check_for_key_count(self):
        count = self.count_keys()[0][0]
        subject = 'Office Keys'
        message = f'There are {count} available keys remaining'
        try:
            send_email(subject, message)
        except Exception as e:
            print(e)

