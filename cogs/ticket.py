import discord
import re
from discord.ext import commands

from data.database import WadsworthDB
from data.jitbit import LocalTicketDB
from data.messages import WadsworthMsg

conection = 'data/wadsworth.db'

class TicketsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channel = 819731985780965376
        self.ticket_url = 'https://support.arizonapipeline.com/helpdesk/Ticket/'
        self.db = LocalTicketDB(conection)
        self.msg = WadsworthMsg()
        
        self.db.run()

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(self.channel)
        await channel.send('Wadsworth here, reporting for duty, coming from Ticket Cog')

    # Commands
    @commands.command()
    async def ticket_ping(self, ctx):
        await ctx.send('Tickets Online')


    @commands.command(name='ticket', description='Lists a ticket based on IssueID input')
    async def list_ticket_detail(self, ctx, ticket):
        await ctx.message.delete()
        await ctx.send(self.msg.debanair_messages(ctx.message.author.display_name))
        ticket = self.db.get_single_ticket_detail(ticket)
        embed = self.pretty_ticket(ctx, ticket)
        await ctx.send(embed=embed)

    @commands.command(name='tickets')
    async def list_current_tickets(self, ctx):
        await ctx.message.delete()
        await ctx.send(self.msg.debanair_messages(ctx.message.author.display_name))
        tickets = self.db.get_current_tickets()
        for ticket in tickets:
            embed = self.pretty_ticket(ctx, ticket)
            await ctx.send(embed=embed)
        await ctx.send(f"That is all. There are currently {len(tickets)} open tickets")

    @commands.command(name='url')
    async def list_ticket_from_url(self, ctx, url, comment_quantity: int=None):
        await ctx.message.delete()
        await ctx.send(self.msg.debanair_messages(ctx.message.author.display_name))
        ticket_id = int(self.extract_ticket_from_url(url))
        ticket = self.db.get_single_ticket_detail(ticket_id)
        embed = self.pretty_ticket(ctx, ticket)
        await ctx.send(embed=embed)

        if comment_quantity:
            ticket_comments = self.db.get_single_ticket_comments(ticket_id)
            i = 0
            for comment in ticket_comments:
                embed = self.pretty_comment(ctx, comment)
                await ctx.send(embed=embed)
                i += 1
                if i == comment_quantity:
                    break


    def pretty_ticket(self, ctx, ticket):
        embed = discord.Embed(
            title=f'**{ticket["Subject"]}**',
            url=f'{self.ticket_url}{ticket["ID"]}',
            color=0x03f8fc,
            timestamp=ctx.message.created_at)
        embed.add_field(name='Tech', value=ticket['Tech'], inline=True)
        embed.add_field(name='Status', value=ticket['Status'], inline=True)
        embed.add_field(name='Subject', value=ticket['Subject'], inline=False)
        embed.add_field(name='Body', value=ticket['Body'], inline=False)
        embed.add_field(name='\u2800', value=('\u2800' * 65), inline=False)
        return embed


    def pretty_comment(self, ctx, comment):
        embed = discord.Embed(
        author=comment['User'],
        color=discord.Color.green()
        )
        embed.add_field(name='User', value=comment['User'], inline=True)
        embed.add_field(name='Tech only', value=comment['Type'], inline=True)
        embed.add_field(name='Message', value=comment['Body'], inline=False)
        embed.set_footer(text='\u2800' * 75)
        return embed


    def extract_ticket_from_url(self, url):
        url = re.sub(self.ticket_url, '', url)
        return url


def setup(bot):
    bot.add_cog(TicketsCog(bot))
