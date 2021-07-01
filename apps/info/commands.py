import discord, os, platform, asyncio
from discord.ext import commands

from core.shared.utils import pretty_ping
from core.shared.messages import  agreement_reactions
import core.config

class InfoCommands(commands.Cog, name='info_commands'):

    def __init__(self, bot):
        self.bot = bot
        self.hidden = []
        if core.config.TESTING:
            self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        else:
            self.channel = self.bot.get_channel(core.config.WADSWORTH_CHANNEL)
        self.ping_channel = self.channel


    # Commands
    @commands.command(name='info-ping', aliases=['-ip'], hidden=True)
    async def info_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Info' module
        """
        embed = pretty_ping(ctx, name=self.__class__.__name__)
        await self.channel.send(embed=embed)

 
    @commands.command(name='help', aliases=['h'])
    async def help(self, ctx):
        """
        List all commands from each loaded cog
        """
        embed = discord.Embed(
            title='Wadsworth Help',
            desciption='List of available commands',
            color=0xE3E3E3,
            timestamp=ctx.message.created_at)
        for cog, commands in self.bot.cogs.items():
            if cog.split('_')[1].lower() not in ['events', 'tasks']:
                cog = self.bot.get_cog(cog)
                commands = cog.get_commands()
                help_commands = [
                    (command.name, command.help)
                    for command in commands
                    if command.name not in self.hidden
                    ]
                help_text = '\n'.join(f'{n} : {h}' for n, h in help_commands)
                cog_title = cog.qualified_name.split('_')[0].title()
                embed.add_field(name=cog_title, value=help_text, inline=False)
                embed.add_field(name='** **', value=f'** **', inline=False)
                embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
        await self.channel.send(f'{ctx.author.mention}')
        msg = await self.channel.send(embed=embed)
        reactions = agreement_reactions
        for reaction in reactions:
            await msg.add_reaction(reaction)



    @commands.command(name='about')
    async def about(self, ctx):
        """
        Returns some general information about Wadsworth
        """
        embed = discord.Embed(
            title='About Wadsworth',
            desciption='Wadsworth General Information',
            color=0xE3E3E3,
            timestamp=ctx.message.created_at)
        embed.add_field(name="Owner", value="Poseidon#4021", inline=True)
        embed.add_field(name='Python Version', value=f'{platform.python_version()}', inline=False)
        embed.add_field(name='Wadsworth Version', value=f'{core.config.VERSION}', inline=False)
        embed.add_field(name='Description', value=f'{core.config.DESCRIPTION}', inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
        await self.channel.send(f'{ctx.author.mention}')
        await self.channel.send(embed=embed)

