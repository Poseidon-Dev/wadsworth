import discord, os
from discord.ext import commands

from core.shared.utils import pretty_ping
import core.config

from .utils import pretty_inventory_list, pretty_division_invetory
from .models import InventoryTable

class InventoryCommands(commands.Cog, InventoryTable, name='inventory_commands'):

    def __init__(self, bot):
        InventoryTable.__init__(self)
        self.bot = bot
        if core.config.TESTING:
            self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        else:
            self.channel = self.bot.get_channel(core.config.INVENTORY_CHANNEL)
        self.ping_channel = self.channel

    # Commands
    @commands.command(name='Inventory-ping', aliases=['-invp'])
    async def inventory_ping(self, ctx):
        """
        Checks to see if commands are reaching the 'Inventory' module
        """
        embed = pretty_ping(ctx, name=self.__class__.__name__)
        await self.ping_channel.send(embed=embed)

    @commands.command(name='inv')
    async def inventory_commands(self, ctx, argument, key=None, column=None):
        if argument in ['-i', 'all']:
            if key:
                await self.read_single_inventory(ctx, key)
            else:
                try:
                    await self.read_inventory(ctx)
                except Exception as e:
                    print(e)
        if column:
            column = f'{column}s'
            if argument in ['-r', 'remove']:
                if not key:
                    await self.channel.send('I need more information')
                else:
                    await self.update_inventory(ctx, key, column, mode='remove')
            
            if argument in ['-a', 'add']:
                if not key:
                    await self.channel.send('I need more information')
                else:
                    await self.update_inventory(ctx, key, column, mode='add')

        if argument in ['-u', 'update']:
            pass
        

    async def read_inventory(self, ctx):
        """
        Returns all data in the inventory table
        """
        inventory = self.select_all()
        for division in inventory:
            await self.channel.send(embed=pretty_inventory_list(ctx, division))

    async def read_single_inventory(self, ctx, key):
        """
        Returns inventory row for a specific division
        """
        division = self.select_by_id(key)
        await self.channel.send(embed=pretty_inventory_list(ctx, division[0]))

    async def update_inventory(self, ctx, key, column, mode):
        inventory = self.update_record(key, column, mode)
        await self.channel.send(f'{mode} instance of {column} from division: {key}')
