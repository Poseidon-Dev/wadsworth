import discord

def pretty_ping(ctx, name):
    """
    Returns an embed for pings for a prettier discord format
    """
    embed = discord.Embed(color=0x333333,
        timestamp=ctx.message.created_at)
    embed.set_footer(text=f"'{name}' ping request by {ctx.message.author}")
    return embed
