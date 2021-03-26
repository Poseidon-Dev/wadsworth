import discord, os, sys

from math import floor, ceil

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

from data import DB

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
        name = f'{employee[1]} {employee[2][:1]} {employee[4]}'
        division = DB().select_row_by_key(table='division_table', key=employee[6])
        
        embed = discord.Embed(
            title=f'**{name}**',
            color=0x03f8fc
        )
        embed.add_field(
            name=f'{employee[0]}',
            value=f"""
            > Division : {division[0][1]}\n> 
            > Status : {employee[7]}\n> 
            > Security : {employee[5]}\n> 
            """ + '\u2800' * 27,
            inline=False)
        embed.set_footer(text=f"'Requested by {ctx.message.author}")
        return embed

    def pretty_assets(self, ctx, key):
        """
        Returns an embed for assets for a prettier discord format
        """
        embed = discord.Embed(
            title=f'Company Property',
            color=0x03f8fc
        )
        assets = DB().select_columns('category, brand, model, serial, status', 'asset_table', where=f'WHERE empid={key}')
        for asset in assets:
            category = DB().select_row_by_key(table='category_table', key=asset[0])[0][1]
            status = DB().select_row_by_key(table='status_table', key=asset[4])[0][1]

            embed.add_field(
                name=category,
                value=f"""
                > Brand : {asset[1]}\n> 
                > Model : {asset[2]}\n> 
                > Key : {asset[3]}\n> 
                > Status : {status}\n
                """ + '\u2800' * 27,
                inline=False
            )
        embed.set_footer(text=f"'Requested by {ctx.message.author}")

        return embed


#     def pretty_table(self, headers, lines):
#         total_width = 65
#         lead = '```'
#         tail = '```'

#         length = int(total_width / len(headers))
#         header = [head + " " * (length - len(head)) for head in headers]
#         head = ''.join(head for head in header)

#         rows = ''
#         for line in lines:
#             rows += " ".join(f'{item}' + " " * (length - len(str(item)) -1) for item in line) + '\n' 
           
#             # test = " ".join(str(i) for i in line) + '\n'

#         tail = '```'
#         response = f"""
# {lead}
# {head}\n
# {rows}
# {tail}
#         """
            

#         return response

