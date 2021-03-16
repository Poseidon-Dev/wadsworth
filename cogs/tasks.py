import discord, os, platform
from discord.ext import commands, tasks

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

class Tasks(commands.Cog, name='scheduled tasks'):

    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.printer.start()

    @commands.command(name='task-ping', aliases=['tp'])
    async def task_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Task' module
        """
        embed = discord.Embed(color=0x333333)
        embed.set_footer(text=f"'Task' ping request by {ctx.message.author}")
        await self.channel.send(embed=embed)

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=5.0)
    async def printer(self):
        print(self.index)
        self.index += 1

    @printer.before_loop
    async def before_printer(self):
        print('waiting...')
        await self.bot.wait_until_ready()

        
def setup(bot):
    bot.add_cog(Tasks(bot))