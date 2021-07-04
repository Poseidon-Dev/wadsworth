import discord, os, platform, asyncio, csv
from discord.ext import commands
import re

from .models import EmployeeTable, EmployeePropertyTable
from .migrations import EmployeePropertyMigrations
from .utils import pretty_property
import core.config
from apps.erp.utils import property_dict, property_emoji_names


class ErpEvents(commands.Cog, EmployeeTable, name='erp_events'):

    def __init__(self, bot):
        EmployeeTable.__init__(self)
        EmployeePropertyMigrations().store()
        self.bot = bot
        if core.config.TESTING:
            self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        else:
            self.channel = self.bot.get_channel(core.config.WADSWORTH_CHANNEL)
        self.ping_channel = self.channel

    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.attachments) == "[]":
            return
        else:
            filename = str(message.attachments).split(' ')[2].split("'")[1]
            filepath = 'media/erp/'
            if filename.startswith('erp') and filename.endswith('.csv'):
                await message.attachments[0].save(fp=f"{filepath}{filename}")
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
            else:
                return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id and payload.emoji.name in property_emoji_names:
            channel = self.bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            for embed in msg.embeds:
                embeds = embed.to_dict()['fields']
                employee_ids = [re.findall('(\d+)', val['value'])[0] for val in embeds]
                for employee in employee_ids:
                    for idx, emoji in property_dict.items():
                        if payload.emoji.name == emoji[1]:
                            record = EmployeePropertyTable().filter('employeeid', employee)
                            records = record.filter('property_type', idx).query()
                            for record in records:
                                await channel.send(embed=pretty_property(record))
