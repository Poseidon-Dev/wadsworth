import os, sys
import discord
from discord.ext import commands, tasks

import data

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

intents = discord.Intents.default()
bot = commands.Bot(config.BOT_PREFIX, intents=intents)

if os.path.isfile('cogs/info.py'):
    bot.remove_command('help')

@bot.event
async def on_ready():
    channel = bot.get_channel(config.BOT_CHANNEL)
    await channel.send("Wadsworth is on his way, he is packing his things.")

    await channel.send("He's looking to bring some extra things with him")
    for extension in config.STARTUP_COGS:
        extension = extension.replace('cogs.', '')
        await channel.send(f'...{extension.capitalize()}')
    
    data.create_and_fill_tables()
    for extension in config.STARTUP_COGS:
        try:
            bot.load_extension(extension)
            extension = extension.replace('cogs.', '')
            await channel.send(f"He packed {extension.capitalize()} module.")
        except Exception as e:
            exception = f'{type(e).__name__}: {e}'
            print(exception)
            extension = extension.replace('cogs.', '')
            await channel.send(f"He couldn't seem to find '{extension.capitalize()}' module.")
    await channel.send('Wadsworth here, reporting for duty!')


bot.run(config.TOKEN)