import discord, os, platform
from discord.ext import commands, tasks

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

from data import JitBitTickets, JitBitTicketComments

class Tasks(commands.Cog, name='scheduled tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.check_for_desk_changes.start()
        self.channel = config.BOT_CHANNEL

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

        # check = JitBitTickets().check_ticket_differences()
        # if check:
        #     JitBitTickets().process_ticket_differences()
        #     JitBitTicketComments().push_comments()
        # else:
        #     print('No ticket changes found')

        
def setup(bot):
    bot.add_cog(Tasks(bot))