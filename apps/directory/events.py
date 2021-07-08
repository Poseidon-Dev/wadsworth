from discord.ext import commands

from apps.directory.utils import directory_emojis_list
from apps.directory.queries import ad_query_by_cn, enable_ad, disable_ad
import core.config


class DirectoryEvents(commands.Cog, name='directory_events'):

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
        return True

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id and payload.emoji.name in directory_emojis_list:
            channel = self.bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id) 
            for embed in msg.embeds:
                embeds = embed.to_dict()['title']
                ad_account = ad_query_by_cn(embeds)
                if payload.emoji.name == 'returning':
                    # enable_ad(ad_account)
                    await channel.send(f'{embeds} enabled')
                if payload.emoji.name == 'exiting':
                    # disable_ad(ad_account)
                    await channel.send(f'{embeds} disabled')