import bs4 as BeautifulSoup
import discord, re

import core.config

def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, features="html.parser")
    cleantext = soup.get_text()
    cleantext = cleantext.replace('\n', '')
    cleantext = cleantext.replace('\t', '')
    cleantext = cleantext.replace('\r', '')
    cleantext = cleantext.replace("'", '')
    cleantext = cleantext.replace("\"", ' ')
    cleantext = cleantext.replace(u'\xa0', u' ')
    return cleantext
    

def pretty_ticket(ctx, ticket):
        """
        Returns an embed for tickets for a prettier discord format
        """
        embed = discord.Embed(
            title=f'**{ticket[2]}**',
            url=f'{core.config.HELPDESK_URL}Ticket/{ticket[0]}',
            color=0x03f8fc,
            timestamp=ctx.message.created_at)
        embed.add_field(name='Tech', value=ticket[1], inline=True)
        embed.add_field(name='Status', value=ticket[3], inline=True)
        embed.add_field(name='Subject', value=ticket[2], inline=False)
        embed.add_field(name='Body', value=ticket[4], inline=False)
        embed.add_field(name='\u2800', value=('\u2800' * 65), inline=False)
        embed.set_footer(text=f"'Requested by {ctx.message.author}")
        return embed


def pretty_comment(ctx, comment):
    """
    Returns an embed for ticket comments for a prettier discord format
    """
    embed = discord.Embed(
    author=comment[2],
    color=discord.Color.green()
    )
    embed.add_field(name='User', value=comment[2], inline=True)
    embed.add_field(name='Tech only', value=comment[3], inline=True)
    embed.add_field(name='Message', value=comment[4], inline=False)
    embed.add_field(name='\u2800', value=('\u2800' * 65), inline=False)
    embed.set_footer(text=f"'Requested by {ctx.message.author}")
    return embed


def extract_ticket_from_url(url_input):
        ticket_url = f'{core.config.HELPDESK_URL}Ticket/'
        return re.sub(ticket_url,"", url_input)
