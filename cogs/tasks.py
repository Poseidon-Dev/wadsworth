import discord, os, platform
from discord.ext import commands, tasks

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

from data import JitBitTickets, JitBitTicketComments
from utils import Pretty

class Tasks(commands.Cog, name='scheduled tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.check_for_desk_changes.start()
        self.channel = config.BOT_CHANNEL
        self.ping_channel = self.bot.get_channel(config.WADSWORTH_CHANNEL)
        

    @commands.command(name='task-ping', aliases=['tp'])
    async def task_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Task' module
        """
        embed = Pretty().pretty_ping(ctx, name=self.__class__.__name__)
        await self.ping_channel.send(embed=embed)

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=10.0)
    async def check_for_desk_changes(self):
        print('checking')
        try:
            ticket = JitBitTickets().check_ticket_differences()
            print(ticket)
            if ticket:
                JitBitTicketComments().push_comment(ticket)
        except Exception as e:
            print(e)

        
def setup(bot):
    bot.add_cog(Tasks(bot))