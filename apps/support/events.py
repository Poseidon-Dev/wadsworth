import re
from discord.ext import commands

import core.config
from apps.support.migrations import JitBitTickets
from apps.support.utils import pretty_ticket

class SupportEvents(commands.Cog, name='support_events'):

    def __init__(self, bot):
        self.bot = bot
        if core.config.TESTING:
            self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        else:
            self.channel = self.bot.get_channel(core.config.WADSWORTH_CHANNEL)
        self.ping_channel = self.channel


    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            if core.config.HELPDESK_URL in message.content:
                ticket_id = re.findall(r'[0-9]+', message.content)
                ticket_detail = JitBitTickets().pull_ticket(str(ticket_id[0]))
                await message.channel.send(embed=pretty_ticket(message, ticket_detail))