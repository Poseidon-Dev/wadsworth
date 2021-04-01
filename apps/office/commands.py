import discord, os, asyncio
from discord.ext import commands

import core.config
from core.shared.utils import pretty_ping
from .utils import pretty_keys
from .models import OfficeTable


class OfficeCommands(commands.Cog, OfficeTable, name='office_commands'):

    def __init__(self, bot):
        OfficeTable.__init__(self)
        self.bot = bot
        if core.config.TESTING:
            self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        else:
            self.channel = self.bot.get_channel(core.config.OFFICE_CHANNEL)
        self.ping_channel = self.channel
        self.timeout = 15

        self.arguments = ['-a', '-r', '-h', '-d', '-m', '-c', 'add', 'read', 'history', 'delete', 'me', 'count']
        self.boolean_choices = ["y", "n", "yes", "no", "yep", "nope", "yea", "nah"]

    # Commands
    @commands.command(name='office-ping', aliases=['-op'])
    async def office_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Office' module
        """
        embed = pretty_ping(ctx, name=self.__class__.__name__)
        await self.ping_channel.send(embed=embed)


    @commands.command(name='key')
    async def office_key_commands(self, ctx, argument, key=None):
        """
        [ARG] [KEY]
            \u2800\u2800Runs functions based on input switch arguments
            \u2800\u2800(-a) : Adds [KEY] to local db
            \u2800\u2800(-d) : Dels [KEY] from local db
            \u2800\u2800(-r) : Reads available keys from local db
            \u2800\u2800(-m) : Gathers and stores key use
            \u2800\u2800(-c) : Returns count of available keys
        """
        if ctx.channel != self.channel:
            await ctx.send('I am terribly sorry, I cannot perform that task within this channel. :disappointed:')
            await ctx.send('Please go to the office-keys channel and I can look into that.')
        else:
            if argument not in self.arguments:
                await self.channel.send('That is not a valid request')
            else:
                author = ctx.author
                if key:
                    # Argument -a
                    if argument in ['-a', 'add']:
                        await self.add_key(ctx, key)

                else:
                    # Argument -d
                    if argument in ['-d', 'delete']:
                        try:
                            await self.channel.send('Which key would you like to delete?')
                            keys = self.read_available()
                            await self.channel.send(embed=pretty_keys(ctx, keys))
                            msg = await self.bot.wait_for(
                                'message',
                                timeout=self.timeout,
                                check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)
                            await self.channel.send(f"Are you positive you'd like to retire key: {msg.content}?")
                            try:
                                del_msg = await self.bot.wait_for(
                                    'message',
                                    timeout=self.timeout,
                                    check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)
                                await self.del_key(ctx, del_msg, msg.content)
                            except asyncio.TimeoutError:
                                await self.channel.send('I suppose not\nI will be here if you need me')
                        except asyncio.TimeoutError:
                            await self.channel.send('I suppose that means you would like to keep them all.')

                    # Argument -r
                    if argument in ['-r', 'read']:
                        keys = self.read_available()
                        if keys:
                            await self.channel.send(embed=pretty_keys(ctx, keys))
                        else:
                            await self.channel.send('I apologize, it appears you are all out of keys.')
                            await asyncio.sleep(1.5)
                            await self.channel.send('You can add more keys with -key -a [KEY] command.')

                    # Argument -m 
                    if argument in ['-m', 'me']:
                        await self.channel.send('What was the email you used?')
                        try:
                            email_msg = await self.bot.wait_for(
                                'message',
                                timeout=self.timeout,
                                check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)
                            try:
                                await self.channel.send('And what was the computer name')
                                comp_msg = await self.bot.wait_for(
                                    'message',
                                    timeout=self.timeout,
                                    check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)
                                office_key = self.deliver_available_key(email_msg, comp_msg, key)
                                await self.channel.send(str(office_key))
                            except asyncio.TimeoutError:
                                await self.channel.send('I suppose you must have forgotten\nI will be here if you need me')
                        except asyncio.TimeoutError:
                            await self.channel.send('I suppose you must have forgotten\nI will be here if you need me')
                        
                    # Arguement -c
                    if argument in ['-c', 'count']:
                        await self.channel.send(f'```There are {self.count_keys()[0][0]} keys left```')

                    # Argument -h
                    if argument in ['-h', 'history']:
                        await self.channel.send('you made it to the dark place of history')
    def add_key(self, ctx, key):
            """
            Adds a key to office_table db
            """
            if len(key) != 29:
                return self.channel.send(f"I do apologize, but I do not believe that '**{key}**' is a valid key") 
            self.insert_key(key)
            return self.channel.send(f'I have added key {key} with the others') 

    def del_key(self, ctx, msg, key):
        """
        Deletes a key from the office_table db based on ID
        """
        if msg.content.lower() in core.config.CONFIRMS:
            self.delete_row_by_key(key)
            return self.channel.send(f'I have set key : {key} in with the other rubbish.')
        if msg.content.lower() in core.config.DENIES:
            return self.channel.send("I'll put it back with the others then")
        
        
    def read_available(self):
        """
        Reads all currently available keys
        """
        return self.select_all_active()


    def deliver_available_key(self, email_msg, comp_msg, key):
        try:
            key = self.retrieve_and_log_key(comp_msg.content.lower(), email_msg.content.lower())
            response = '```' + 'Here is your key : ' + key[0][1] + '```'
        except Exception as e:
            response = 'No keys available'
        return response