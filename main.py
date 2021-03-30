import os, sys, importlib
import discord
from discord.ext import commands, tasks

from core import config, messages

bot = config.BOT

@bot.event
async def on_ready():
    """
    Initializes bot and all application modeules specified in config
    """
    channel = config.BOT.get_channel(config.BOT_CHANNEL)
    await channel.send(messages.intro)

    # Load Applications
    for extension in config.STARTUP_COGS:
        try:
            importlib.import_module(extension)
            bot.load_extension(extension)
            extension = extension.replace('apps.', '')
            print(f'{extension} loaded')
        except Exception as e:
            exception = f'Could not load {extension}'
            print(exception)

    # await channel.send(messages.ready)



config.BOT.run(config.TOKEN)