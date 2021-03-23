import discord, re, os, sys
from discord.ext import commands

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

from data import TicketTable, TicketCommentTable, WadsworthMsg
from utils import Pretty
class TicketsCog(commands.Cog, TicketTable, name='tickets'):

    def __init__(self, bot):
        TicketTable.__init__(self)
        self.bot = bot
        self.channel = self.bot.get_channel(config.BOT_CHANNEL)

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.channel
        await channel.send('Wadsworth here, reporting for duty, coming from Ticket Cog')

    # Commands
    @commands.command(name='ticket-ping')
    async def tickets_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Tickets' module
        """
        embed = Pretty().pretty_ping(ctx, name=self.__class__.__name__)
        await ctx.send(embed=embed)


    @commands.command(name='ticket', description='Lists a ticket based on IssueID input')
    async def list_ticket_detail(self, ctx, ticket):
        """
        [TICKETID]
            \u2800\u2800Returns a ticket base on TicketID input
        """
        await ctx.message.delete()
        await ctx.send(WadsworthMsg().debanair_messages(ctx.message.author.display_name))
        ticket = self.select_row_by_key(self.table, ticket)
        embed = Pretty().pretty_ticket(ctx, ticket[0])
        await ctx.send(embed=embed)

    @commands.command(name='tickets')
    async def list_current_tickets(self, ctx):
        """
        Returns all current tickets stored in local db in pretty format 
        """
        await ctx.message.delete()
        await ctx.send(WadsworthMsg().debanair_messages(ctx.message.author.display_name))
        tickets = self.select_all()
        for ticket in tickets:
            embed = Pretty().pretty_ticket(ctx, ticket)
            await ctx.send(embed=embed)
        await ctx.send(f"That is all. There are currently {len(tickets)} open tickets")

    @commands.command(name='url')
    async def list_ticket_from_url(self, ctx, url, comment_quantity: int=None):
        """
        [URL] [COUNT]
            \u2800\u2800Returns a ticket base on URL input
            \u2800\u2800Returns [COUNT] of recent comments (op)
        """
        await ctx.message.delete()
        await ctx.send(WadsworthMsg().debanair_messages(ctx.message.author.display_name))
        ticket_id = int(self.extract_ticket_from_url(url))
        print(ticket_id)
        ticket = self.select_row_by_key(self.table, ticket_id)
        embed = Pretty().pretty_ticket(ctx, ticket[0])
        await ctx.send(embed=embed)

        if comment_quantity:
            ticket_comments = self.select_all(table="ticket_comments", where=f"WHERE ticket_id = '{ticket_id}'")
            i = 0
            print(ticket_comments)
            for comment in ticket_comments:
                embed = Pretty().pretty_comment(ctx, comment)
                await ctx.send(embed=embed)
                i += 1
                if i == comment_quantity:
                    break


    def extract_ticket_from_url(self, url_input):
        ticket_url = f'{config.HELPDESK_URL}Ticket/'
        return re.sub(ticket_url,"", url_input)


def setup(bot):
    bot.add_cog(TicketsCog(bot))
