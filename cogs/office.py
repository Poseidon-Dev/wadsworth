import discord, os, sys
from discord.ext import commands
from datetime import date

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

from data import OfficeTable, WadsworthMsg

class OfficeCog(commands.Cog, OfficeTable, name='office'):

    def __init__(self, bot):
        OfficeTable.__init__(self)
        self.bot = bot
        self.channel = self.bot.get_channel(config.BOT_CHANNEL)
        self.arguments = ['-a', '-r', '-h', '-d', '-m', '-c' 'add', 'read', 'history', 'delete', 'me', 'count']
        self.boolean_choices = ["y", "n", "yes", "no", "yep", "nope", "yea", "nah"]

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(self.channel)
        await channel.send('Wadsworth here, reporting for duty, coming from Office Cog')


    # Commands
    @commands.command()
    async def office_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Office' module
        """
        await ctx.send('Office Online')


    @commands.command(name='key')
    async def office_key_commands(self, ctx, argument, key=None):
        """
        Add (-a), delete (-d), Read available (-a), Retrieve and retire active key (-m), Show key count (-c)
            \u2800\u2800\u2800ex: !key -a
        """
        await ctx.message.delete()
        if argument not in self.arguments:
            await ctx.send('That is not a valid request')
        else:
            if key:
                # Argument -a
                if argument in ['-a', 'add']:
                    if len(key) != 29:
                        await ctx.send(f"I do apologize, but I do not believe that '**{key}**' is a valid key") 
                    else:
                        self.insert_key(key)
                        await ctx.send(f'I have added key {key} with the others') 

                # Argument -d
                if argument in ['-d', 'delete']:
                    await ctx.send(f"Are you positive you'd like to retire key: {key}?")
                    msg = await self.bot.wait_for('message')
                    if msg.content.lower() in config.CONFIRMS:
                        self.delete_row_by_key(key)
                        await ctx.send(f'I have set key : {key} in with the other rubbish.')
                    if msg.content.lower() in config.DENIES:
                        await ctx.send("I'll put it back with the others then")
                    else:
                        await ctx.send("I'm not sure I understand your response")

            else:
                # Argument -r
                if argument in ['-r', 'read']:
                    keys = self.select_all_active()
                    await ctx.send(embed=self.pretty_keys(keys))

                # Argument -m 
                if argument in ['-m', 'me']:
                    await ctx.send('What was the email you used?')
                    email_msg = await self.bot.wait_for('message')

                    await ctx.send('And what was the computer name')
                    comp_msg = await self.bot.wait_for('message')

                    try:
                        key = self.retrieve_and_log_key(comp_msg.content.lower(), email_msg.content.lower())
                        response = '```' + 'Here is your key : ' + key[0][1] + '```'
                    except Exception as e:
                        response = 'No keys available'
                    await ctx.send(f'There are {self.count_keys()[0][0]} left')
                    await ctx.send(response)
                
                # Arguement -c
                if argument in ['-c', 'count']:
                    await ctx.send(f'```There are {self.count_keys()[0][0]} keys left```')


    def pretty_keys(self, keys):
        embed = discord.Embed(
            title='Office Keys',
            color=0x03f8fc
        )
        for key in keys:
            id_value = f'{key[0]}' + '\u2800' * 50
            embed.add_field(name='ID', value=id_value, inline=False)
            embed.add_field(name='Key', value=key[1], inline=False)
        return embed


def setup(bot):
    bot.add_cog(OfficeCog(bot))
