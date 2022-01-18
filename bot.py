import os, sys, importlib
import discord
from discord.ext import commands, tasks

from core import config, messages
from core.shared.utils import Timer

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
            t = Timer(str(extension))
            t.start()
            importlib.import_module(extension)
            bot.load_extension(extension)
            extension = extension.replace('apps.', '')
            t.stop()
        except Exception as e:
            exception = f'Could not load {extension}\n{e}'
            print(exception)

    await channel.send(messages.ready)


if __name__ == "__main__":
    config.BOT.run(config.TOKEN)
