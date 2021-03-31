import discord

def pretty_keys(ctx, keys):
    """
    Returns an embed for keys for a prettier discord format
    """
    embed = discord.Embed(
        title='Office Keys',
        color=0x03f8fc,
        timestamp=ctx.message.created_at)
    for key in keys:
        id_value = f'{key[0]}' + '\u2800' * 50
        embed.add_field(name='ID', value=id_value, inline=False)
        embed.add_field(name='Key', value=key[1], inline=False)
        embed.set_footer(text=f"'Requested by {ctx.message.author}")
    return embed

