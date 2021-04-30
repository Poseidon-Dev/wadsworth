from apps.inventory.commands import InventoryCommands
from apps.inventory.events import InventoryEvents
from apps.inventory.models import InventoryTable

def setup(bot):
    bot.add_cog(InventoryCommands(bot))
    bot.add_cog(InventoryEvents(bot))
    InventoryTable().run()
