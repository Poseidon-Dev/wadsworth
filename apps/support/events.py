import re
from discord.ext import commands

import core.config
from apps.support.migrations import JitBitTickets
from apps.support.utils import pretty_ticket, support_dict, support_emoji_list
from apps.erp.models import EmployeePropertyTable

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

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id and payload.emoji.name in support_emoji_list:
            channel = self.bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            for embed in msg.embeds:
                embeds = embed.to_dict()['url']
                ticket_id = re.findall(r'[0-9]+', embeds)
                pwd_rtn = ''
                ticket_detail = JitBitTickets().pull_ticket(str(ticket_id[0]))
                employee_id = re.findall('\d+', ticket_detail.get("Subject"))
                email_pwd = EmployeePropertyTable().filter('employeeid', employee_id[0]).filter('property_type', 9).query()
                if email_pwd:
                    for pwd in email_pwd:
                        email_pwd_print = f'Account: {pwd[4]}\nPassword: {pwd[2]}\n\n'
                        pwd_rtn += email_pwd_print
                if pwd_rtn:
                    JitBitTickets().post_ticket_comment(str(ticket_id[0]), pwd_rtn)
                    JitBitTickets().update_ticket(str(ticket_id[0]), 3)