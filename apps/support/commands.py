import discord, os
from discord.ext import commands

from core.shared.utils import pretty_ping
import core.config
from .utils import pretty_ticket, pretty_comment, extract_ticket_from_url
from .models import TicketTable, TicketCommentTable

class SupportCommands(commands.Cog, TicketTable, name='Support'):

    def __init__(self, bot):
        TicketTable.__init__(self)
        self.bot = bot
        if core.config.TESTING:
            self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        else:
            self.channel = self.bot.get_channel(core.config.WADSWORTH_CHANNEL)
        self.ping_channel = self.channel

    # Commands
    @commands.command(name='support-ping', aliases=['-sp'])
    async def support_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Support' module
        """
        embed = pretty_ping(ctx, name=self.__class__.__name__)
        await self.ping_channel.send(embed=embed)


    @commands.command(name='ticket', description='Lists a ticket based on IssueID input')
    async def list_ticket_detail(self, ctx, ticket):
        """
        [TICKETID]
            \u2800\u2800Returns a ticket base on TicketID input
        """
        await ctx.message.delete()
        # await ctx.send(WadsworthMsg().debanair_messages(ctx.message.author.display_name))
        ticket = self.select_by_id(ticket, self.table)
        embed = pretty_ticket(ctx, ticket[0])
        await ctx.send(embed=embed)


    @commands.command(name='tickets')
    async def list_current_tickets(self, ctx):
        """
        Returns all current tickets stored in local db in pretty format 
        """
        await ctx.message.delete()
        # await ctx.send(WadsworthMsg().debanair_messages(ctx.message.author.display_name))
        tickets = self.select_all()
        for ticket in tickets:
            embed = pretty_ticket(ctx, ticket)
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
        # await ctx.send(WadsworthMsg().debanair_messages(ctx.message.author.display_name))
        ticket_id = int(extract_ticket_from_url(url))
        ticket = self.select_by_id(ticket_id, self.table)
        embed = pretty_ticket(ctx, ticket[0])
        await ctx.send(embed=embed)

        if comment_quantity:
            ticket_comments = self.select_all(table="ticket_comments", where=f"WHERE ticket_id = '{ticket_id}'")
            i = 0
            for comment in ticket_comments:
                embed = pretty_comment(ctx, comment)
                await ctx.send(embed=embed)
                i += 1
                if i == comment_quantity:
                    break