import discord, os
from datetime import datetime
from discord.ext import commands

from core.shared.utils import pretty_ping
import core.config

from apps.scheduler.utils import pretty_scheduler, pretty_scheduler_from_db
from apps.scheduler.models import SchedulerTable, ScheduleCalender, Participant, Schedule

class SchedulerCommands(commands.Cog, name='scheduler_commands'):

    def __init__(self, bot):
        self.bot = bot
        self.timeout = 300
        if core.config.TESTING:
            self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        else:
            self.channel = self.bot.get_channel(core.config.WADSWORTH_CHANNEL)
            self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        self.ping_channel = self.channel

    @commands.command(name='scheduler-ping', aliases=['-tp'])
    async def scheduler_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Scheduler' module
        """
        embed = pretty_ping(ctx, name=self.__class__.__name__)
        await self.ping_channel.send(embed=embed)

    @commands.command(name='sched', aliases=['-s'])
    async def schedule(self, ctx):
        """
        Create a new scheduled task
        """
        creator = Participant(ctx.author.id)

        await self.channel.send('Title of the task?')
        title = await self.bot.wait_for('message', timeout=self.timeout, check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)

        await self.channel.send('Description?')
        body = await self.bot.wait_for('message', timeout=self.timeout, check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)

        await self.channel.send('Date? (yyyy-mm-dd)')
        date = await self.bot.wait_for('message', timeout=self.timeout, check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)

        print(ctx.channel.id)
        print(creator.participant_id)

        cal = ScheduleCalender()
        cal.create_event(ctx.channel.id, title.content.upper(), body.content.upper(), date.content.upper(), creator.participant_id)


        # scheduler = SchedulerTable()
        # await self.channel.send('Title of the task?')
        # title = await self.bot.wait_for('message', timeout=self.timeout, check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)

        # await self.channel.send('Description?')
        # body = await self.bot.wait_for('message', timeout=self.timeout, check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)

        # await self.channel.send('Date? (yyyy-mm-dd)')
        # date = await self.bot.wait_for('message', timeout=self.timeout, check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)

        # await self.channel.send('Time? (hh:mm AM/PM)')
        # time = await self.bot.wait_for('message', timeout=self.timeout, check=lambda msg: msg.author == ctx.author and msg.channel == ctx.channel)
        # date_string = date.content + ' ' + time.content.replace(' ','')
        # format = '%Y-%m-%d %I:%M%p'
        # date_output = datetime.strptime(date_string, format)
        # if date_output > datetime.now():
        #     data = [title.content.upper(), body.content.capitalize(), date_output]
        #     await self.channel.send(embed=pretty_scheduler(ctx, data))
        #     data = [
        #         ('type', 'Task'),
        #         ('title', title.content),
        #         ('body', body.content),
        #         ('datetime', date_output),
        #         ]
        #     scheduler.insert(data)
        # else:
        #     await self.channel.send(f"I'm sorry, it seems that that is in the past")

    # @commands.command(name='schedule-upcoming', aliases=['su'])
    # async def schedule(self, ctx):
    #     """
    #     Prints current schedules
    #     """
    #     scheduler = SchedulerTable()
    #     data = scheduler.select_first().query()
    #     await self.channel.send(embed=pretty_scheduler_from_db(data))