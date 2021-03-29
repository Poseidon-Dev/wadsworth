import discord, os, sys, requests
import re
from discord.ext import commands
from random import randint


if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

from utils import Pretty


class PasswordCog(commands.Cog, name='password'):

    def __init__(self, bot):
        self.bot = bot
        self.channel = self.bot.get_channel(config.EMAIL_CHANNEL)
        self.ping_channel = self.bot.get_channel(config.WADSWORTH_CHANNEL)
        self.arguments = ['-a', '-r', '-h', '-d', '-m', '-c' 'add', 'read', 'history', 'delete', 'me', 'count']
        self.boolean_choices = ["y", "n", "yes", "no", "yep", "nope", "yea", "nah"]
        self.all_words = requests.get(config.WORD_SITE).content.splitlines()
        self.words = [word.decode('utf-8') for word in self.all_words if len(word) > 3 and len(word) < 6]


    # Commands
    @commands.command(name='pass-ping')
    async def password_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Password' module
        """
        embed = Pretty().pretty_ping(ctx, name=self.__class__.__name__)
        await self.ping_channel.send(embed=embed)


    @commands.command(name='pass')
    async def password_module(self, ctx):
        """
        Generates two random words between 4 and 5 charactes long, changes (a,e,s) and adds random int between 100 and 999
        """
        if ctx.channel != self.channel:
            await ctx.send('I am terribly sorry, I cannot perform that task within this channel. :disappointed:')
            await ctx.send('Please go to the email channel and I can look into that.')
        else:
            word = f'{self.words[randint(1,2500)].capitalize()}{self.words[randint(1,2500)]}{randint(100, 999)}'
            word = re.sub('a', '@', word)
            word = re.sub('e', '3', word)
            word = re.sub('s', '5', word)
            await self.channel.send(f'```Your random password: {word}```')
   

def setup(bot):
    bot.add_cog(PasswordCog(bot))