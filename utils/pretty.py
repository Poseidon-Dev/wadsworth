import discord, os, sys

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

class Pretty:

    def pretty_ping(self, ctx, name):
        """
        Returns an embed for pings for a prettier discord format
        """
        embed = discord.Embed(color=0x333333)
        embed.set_footer(text=f"'{name}' ping request by {ctx.message.author}")
        return embed


    def pretty_ticket(self, ctx, ticket):
        """
        Returns an embed for tickets for a prettier discord format
        """
        embed = discord.Embed(
            title=f'**{ticket[2]}**',
            url=f'{config.HELPDESK_URL}Ticket/{ticket[0]}',
            color=0x03f8fc,
            timestamp=ctx.message.created_at)
        embed.add_field(name='Tech', value=ticket[1], inline=True)
        embed.add_field(name='Status', value=ticket[3], inline=True)
        embed.add_field(name='Subject', value=ticket[2], inline=False)
        embed.add_field(name='Body', value=ticket[4], inline=False)
        embed.add_field(name='\u2800', value=('\u2800' * 65), inline=False)
        embed.set_footer(text=f"'Requested by {ctx.message.author}")
        return embed


    def pretty_comment(self, ctx, comment):
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


    def pretty_keys(self, ctx, keys):
        """
        Returns an embed for keys for a prettier discord format
        """
        embed = discord.Embed(
            title='Office Keys',
            color=0x03f8fc
        )
        for key in keys:
            id_value = f'{key[0]}' + '\u2800' * 50
            embed.add_field(name='ID', value=id_value, inline=False)
            embed.add_field(name='Key', value=key[1], inline=False)
            embed.set_footer(text=f"'Requested by {ctx.message.author}")
        return embed

    def pretty_employee(self, ctx, employee):
        """
        Returns an embed for an employee for a prettier discord format
        """
        print(employee)
        embed = discord.Embed(
            title=employee[0],
            color=0x03f8fc
        )
        embed.add_field(name='First', value=employee[1], inline=True)
        embed.add_field(name='Middle', value=employee[2], inline=True)
        embed.add_field(name='Last', value=employee[4], inline=True)
        embed.add_field(name='Security', value=employee[5], inline=True)
        embed.add_field(name='\u2800', value=('\u2800' * 65), inline=False)
        embed.set_footer(text=f"'Requested by {ctx.message.author}")
        return embed