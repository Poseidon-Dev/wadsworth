import discord

from apps.base.models import Database

def pretty_assets(ctx, key):
    """
    Returns an embed for assets for a prettier discord format
    """
    embed = discord.Embed(
        title=f'Company Property',
        color=0x03f8fc,
        timestamp=ctx.message.created_at)
    assets = Database().select_columns('category, brand, model, serial, status', 'asset_table', where=f'WHERE empid={key}')
    for asset in assets:
        category = Database().select_row_by_key(table='category_table', key=asset[0])[0][1]
        status = Database().select_row_by_key(table='status_table', key=asset[4])[0][1]

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
    embed.set_footer(text=f"Requested by {ctx.message.author.display_name}")

    return embed