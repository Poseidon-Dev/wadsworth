import discord
from apps.erp.utils import property_dict

def pretty_transfer(employee):
    name = f'Employee Transfer - {employee.employee_id} '
    from_d = employee.division
    embed = discord.Embed(
        title=f'**{name}**' + '\u2800' * (35 - len(name)),
        color=0x03f8fc,)
    embed.add_field(name='Name', value=employee.full_name, inline=False)
    embed.add_field(name='From', value=from_d, inline=True)
    embed.add_field(name='To', value=from_d, inline=True)
    employee_property = employee.company_property
    if employee_property:
        for e in employee_property:
            prop = property_dict.get(e[3])[1].capitalize()
            embed.add_field(
            name=prop,
            value=f"""
            > Description : {e[4]} 
            > Control : {e[2]} 
            """ + '\u2800' * 27,
            inline=False)
    return embed
