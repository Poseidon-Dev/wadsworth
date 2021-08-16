import discord, os, platform, asyncio, csv
from discord.ext import commands
import re

import core.config
from apps.verizon.utils import verizon_csv, ALLOWED_DIVISIONS, OUT_REPORTS
class VerizonEvents(commands.Cog, name='verizon_events'):

    def __init__(self, bot):
        self.bot = bot
        if core.config.TESTING:
            self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        else:
            self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        self.ping_channel = self.channel

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.attachments) == "[]":
            return
        else:
            filename = str(message.attachments).split(' ')[2].split("'")[1]
            filepath = 'media/verizon/'
            if filename.lower().startswith('verizon') and filename.endswith('.csv'):
                await message.attachments[0].save(fp=f"{filepath}{filename}")
                await self.channel.send('Got the csv')
                files = verizon_csv()
                if files == 'COMPLETE':
                    for div in OUT_REPORTS:
                        await self.channel.send(file=discord.File(f'{filepath}{div}.csv'))
                else:
                    await self.channel.send(files[1])
                    for div in files[0]:
                        await self.channel.send(div)
            else:
                return
