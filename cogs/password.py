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
        self.channel = self.bot.get_channel(config.BOT_CHANNEL)
        self.arguments = ['-a', '-r', '-h', '-d', '-m', '-c' 'add', 'read', 'history', 'delete', 'me', 'count']
        self.boolean_choices = ["y", "n", "yes", "no", "yep", "nope", "yea", "nah"]
        self.all_words = requests.get(config.WORD_SITE).content.splitlines()
        self.words = [word.decode('utf-8') for word in self.all_words if len(word) > 3 and len(word) < 6]

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(self.channel)
        await channel.send('Wadsworth here, reporting for duty, coming from Password Cog')


    # Commands
    @commands.command(name='pass-ping')
    async def password_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Password' module
        """
        embed = Pretty().pretty_ping(ctx, name=self.__class__.__name__)
        await ctx.send(embed=embed)

    @commands.command(name='pass')
    async def password_module(self, ctx):
        """
        Generates two random words between 4 and 5 charactes long, changes (a,e,s) and adds random int between 100 and 999
        """
        word = f'{self.words[randint(1,2500)].capitalize()}{self.words[randint(1,2500)]}{randint(100, 999)}'
        word = re.sub('a', '@', word)
        word = re.sub('e', '3', word)
        word = re.sub('s', '5', word)
        await ctx.send(f'```Your random password: {word}```')
   

def setup(bot):
    bot.add_cog(PasswordCog(bot))