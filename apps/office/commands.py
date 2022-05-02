import discord, os, asyncio
from discord.ext import commands

import core.config
from core.shared.utils import pretty_ping
from .utils import pretty_keys
from .models import OfficeTable

from core.shared.utils import send_email


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

        self.arguments = ['-a', '-r', '-h', '-d', '-m', '-c', '-b', 'add', 'read', 'history', 'delete', 'me', 'count', 'brion']
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
                            await self.delete_key_checks(ctx, key)
                        except asyncio.TimeoutError:
                            await self.channel.send('I suppose that means you would like to keep them all.')

                    # Argument -r
                    if argument in ['-r', 'read']:
                        try:
                            await self.read_available(ctx)
                        except Exception as e:
                            print(e)

                    # Argument -m 
                    if argument in ['-m', 'me']:
                        try:
                            await self.retrieve_key_check(ctx, key)
                        except asyncio.TimeoutError:
                            await self.channel.send('I suppose you must have forgotten\nI will be here if you need me')
                        
                    # Arguement -c
                    if argument in ['-c', 'count']:
                        await self.channel.send(f'```There are {self.count_available()} keys left```')

                    # Argument -h
                    if argument in ['-h', 'history']:
                        await self.channel.send('you made it to the dark place of history')

                     # Argument -b
                    if argument in ['-b', 'brion']:
                        await self.channel.send('Pinging')
                        send_email('Office', 'Someone pinged you in discord')

    def add_key(self, ctx, key):
            """
            Adds a key to office_table db
            """
            if len(key) != 29:
                return self.channel.send(f"I do apologize, but I do not believe that '**{key}**' is a valid key")
            response = self.insert([('office_keys', key), ('available', 1)])
            if response is True or response == '':
                return self.channel.send(f'I have added key {key} with the others') 
            else:
                return self.channel.send('That key already exist')

    async def delete_key_checks(self, ctx, key):
        await self.channel.send('Which key would you like to delete?')
        keys = self.available().query()
        await self.channel.send(embed=pretty_keys(ctx, keys))
        msg = await self.bot.wait_for(
            'message',
            timeout=self.timeout,
            check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)
        if self.check_if_id_exists(msg.content):
            await self.channel.send(f"Are you positive you'd like to retire key: {msg.content}?")
            try:
                del_msg = await self.bot.wait_for(
                    'message',
                    timeout=self.timeout,
                    check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)
                await self.del_key(del_msg, msg.content)
            except asyncio.TimeoutError:
                await self.channel.send('I suppose not\nI will be here if you need me')
        else:
            await self.channel.send("That's not a valid key")
        

    def del_key(self, msg, key):
        """
        Deletes a key from the office_table db based on ID
        """
        if msg.content.lower() in core.config.CONFIRMS:
            command = OfficeTable().filter(col='id', val=key)
            del_com = command.delete(command)
            return self.channel.send(f'I have set key : {key} in with the other rubbish.')
        if msg.content.lower() in core.config.DENIES:
            return self.channel.send("I'll put it back with the others then")
        
        
    async def read_available(self, ctx):
        """
        Reads all currently available keys
        """
        keys = self.available().query()
        if keys:
            await self.channel.send(embed=pretty_keys(ctx, keys))
        else:
            await self.channel.send('I apologize, it appears you are all out of keys.')
            await asyncio.sleep(1.5)
            await self.channel.send('You can add more keys with -key -a [KEY] command.')


    def check_if_id_exists(self, key):
        """
        Checks if the pkey exists
        """
        return self.filter(key).query()


    async def retrieve_key_check(self, ctx, key):
        """
        CLI command checking for key retrival command inputs
        If a user stalls, it closes the task otherwise continues
        to retrieve and collect input
        """
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


    def deliver_available_key(self, email_msg, comp_msg, key):
        try:
            update = [
                ('computer_name', comp_msg.content.lower()),
                ('email', email_msg.content.lower()),
                ]
            key = OfficeTable().retrieve_and_log_key(update=update)
            response = '```' + 'Here is your key : ' + key[0][1] + '```'
        except Exception as e:
            response = f'No keys available: {e}'
        return response