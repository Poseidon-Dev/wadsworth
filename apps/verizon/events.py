import discord, os, platform, asyncio, csv
from discord.ext import commands
import re

import core.config
from apps.verizon.utils import verizon_csv

verizon_csv()

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
                comment = f'''
                with open(f'{filepath}{filename}', 'r') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    next(csv_reader)
                    output = []
                    for row in csv_reader:
                        employees = self.fetch_like_first_last(row[0].title(), row[1].title())
                        for employee in employees:
                            output.append(employee)
                    with open(f'{filepath}export_{filename}', 'w') as out:
                        csv_out = csv.writer(out)
                        item_length = len(output[0])
                        for row in output:
                            csv_out.writerow(row)
                    await self.channel.send(file=discord.File(f'{filepath}export_{filename}'))
                    '''
            else:
                return
