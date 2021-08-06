from datetime import datetime
import discord
from discord.ext import commands, tasks

import core.config
from core.shared.utils import Timer

from apps.scheduler.models import SchedulerTable
from apps.scheduler.utils import pretty_scheduler_from_db

class SchedulerTasks(commands.Cog, name='scheduler_tasks'):

    def __init__(self, bot):
        self.bot = bot
        # self.check_active_tasks.start()
        self.channel = self.bot.get_channel(core.config.SCHEDULER_CHANNEL)

    @tasks.loop(seconds=10.0)
    async def check_active_tasks(self):
        """
        Reads active tasks and posts them to self.channel
        If the message already exists, edit. 
        If no longer active, remove
        If not within the dataset, remove
        """
        timer = Timer('check tasks')
        timer.start()
        scheduler = SchedulerTable()
        dataset = scheduler.filter('status', 1).query()
        history = await self.channel.history(limit=50).flatten()
        data_check = [f'{data[1]}-{data[2]}' for data in dataset]
        history_check = [f'{msg.channel.id}-{msg.id}' for msg in history]
        add = list(set(data_check) - set(history_check))
        remove = list(set(history_check) - set(data_check))

        for data in dataset:
            key = f'{data[1]}-{data[2]}'
            if key in add:
                message = await self.channel.send(embed=pretty_scheduler_from_db(data))
                record = SchedulerTable().filter(val=data[0]).query()
                scheduler = SchedulerTable()
                command = scheduler.update_record(record, [('channel_id', message.channel.id), ('message_id', message.id)])
                scheduler.execute(command)
        for msg in history:
            key = f'{msg.channel.id}-{msg.id}'
            if key in remove:
                await msg.delete()
        timer.stop()


