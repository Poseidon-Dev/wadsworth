from apps.transfers.commands import TransfersCommands
from apps.transfers.events import TransfersEvents
from apps.transfers.models import TransfersTable
from apps.transfers.tasks import TransfersTasks

def setup(bot):
    # TransfersTable().build()
    bot.add_cog(TransfersTasks(bot))