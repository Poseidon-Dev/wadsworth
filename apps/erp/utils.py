import discord 

from apps.base.models import Database

def pretty_employee(ctx, employee):
    """
    Returns an embed for an employee for a prettier discord format
    """
    name = f'{employee[1]} {employee[2][:1]} {employee[4]}'
    division = Database().select_by_id(table='division_table', key=employee[6])
    
    embed = discord.Embed(
        title=f'**{name}**',
        color=0x03f8fc,
        timestamp=ctx.message.created_at)
    embed.add_field(
        name=f'{employee[0]}',
        value=f"""
        > Division : {division[0][1]}\n> 
        > Status : {employee[7]}\n> 
        > Security : {employee[5]}\n> 
        """ + '\u2800' * 27,
        inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    return embed

def clean_name(name):
    name = name.replace("'", '')
    return name