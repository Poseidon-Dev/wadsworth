import discord

def pretty_inventory_list(ctx, division):
    """
    Returns an embed for inventory for a prettier discord format
    """
    title = f'{division[1]} Inventory' + '\u2800' * 30
    embed = discord.Embed(
        title=title,
        color=0xdfc430,
        timestamp=ctx.message.created_at
    )
    embed.add_field(name='Desktop', value=division[2], inline=True)
    embed.add_field(name='Laptop', value=division[3], inline=True)
    embed.add_field(name='Monitors', value=division[4], inline=True)
    embed.add_field(name='Auxiltery', value=division[5], inline=True)
    embed.add_field(name='Phones', value=division[6], inline=True)
    embed.add_field(name='iPads', value=division[7], inline=True)
    embed.add_field(name='\u2800', value='\u2800', inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
    return embed

def pretty_division_invetory(ctx, division):
    """
    Returns an embed for inventory for a prettier discord format
    """
    title = f'{division[1]} Inventory' + '\u2800' * 30
    embed = discord.Embed(
        title=title,
        color=0xdfc430,
        timestamp=ctx.message.created_at
    )
    embed.add_field(name='Desktop', value=division[2], inline=True)
    embed.add_field(name='Laptop', value=division[3], inline=True)
    embed.add_field(name='Monitors', value=division[4], inline=True)
    embed.add_field(name='Auxiltery', value=division[5], inline=True)
    embed.add_field(name='Phones', value=division[6], inline=True)
    embed.add_field(name='iPads', value=division[7], inline=True)
    embed.add_field(name='\u2800', value='\u2800', inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")
    return embed