import discord, os, platform, asyncio
from discord.ext import commands

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

from data import WadsworthMsg
from utils import Pretty, Validators

class Help(commands.Cog, name='help'):

    def __init__(self, bot):
        self.bot = bot
        self.ping_channel = self.bot.get_channel(config.WADSWORTH_CHANNEL)
        self.hidden = ['ping', 'futures', '/?']
        if config.TESTING:
            self.channel = self.bot.get_channel(config.BOT_CHANNEL)
        else:
            self.channel = self.bot.get_channel(config.WADSWORTH_CHANNEL)

    
    # Events
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == '/?':
            await message.channel.send(WadsworthMsg().trash_talk())
        

    # Commands
    @commands.command(name='help-ping', aliases=['hp'])
    async def info_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Help' module
        """
        embed = Pretty().pretty_ping(ctx, name=self.__class__.__name__)
        await self.ping_channel.send(embed=embed)


    @commands.command(name='help', aliases=['h'])
    async def help(self, ctx):
        """
        List all commands from each loaded cog
        """
        embed = discord.Embed(
            title='Wadsworth Help',
            desciption='List of available commands',
            color=0xE3E3E3) 
        for cog in self.bot.cogs:
            cog = self.bot.get_cog(cog)
            commands = cog.get_commands()
            help_commands = [
                (command.name, command.help)
                for command in commands
                if command.name not in self.hidden
                ]
            help_text = '\n'.join(f'{n} : {h}' for n, h in help_commands)
            embed.add_field(name=f'{cog.qualified_name.capitalize()}', value=help_text, inline=False)
            embed.add_field(name='** **', value=f'** **', inline=False)
            embed.set_footer(text=f"'Requested by {ctx.message.author}")
        await self.channel.send(f'{ctx.author.mention}')
        await self.channel.send(embed=embed)


    @commands.command(name='about', aliases=['readme', '-i'])
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
        embed.add_field(name='Wadsworth Version', value=f'{config.VERSION}', inline=False)
        embed.add_field(name='Description', value=f'{config.DESCRIPTION}', inline=False)
        embed.set_footer(text=f"'Requested by {ctx.message.author}")
        await self.channel.send(f'{ctx.author.mention}')
        await self.channel.send(embed=embed)


    @commands.command(name='futures', aliases=['-f'])
    async def futures(self, ctx):
        """
        Returns the proposed future updates
        """
        features = [
            ('Waypoint', 'Waypoint API integration'),
            ('Ticket History', 'Ticket history lookups'),
            ('Office Integrations', 'Add and remove office keys'),
            ('Email', 'Email password storage'),
            ('Password', 'Password generator'),
            ('Devices', 'Device management system'),
            ('ECMS', 'eCMS API integration for a whois lookup')
        ]
        embed = discord.Embed(
            title='Future Updates',
            desciption='Wadsworth Updates',
            color=0xE3E3E3
        )
        for feature in features:
            embed.add_field(name=feature[0], value=feature[1], inline=False)
            embed.add_field(name='** **', value=f'** **', inline=False)
        await ctx.send(embed=embed)
   
 
        
def setup(bot):
    bot.add_cog(Help(bot))