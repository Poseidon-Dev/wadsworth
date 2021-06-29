from apps.support.commands import SupportCommands
from apps.support.events import SupportEvents

from apps.support.models import TicketTable


def setup(bot):
    TicketTable().build()
    bot.add_cog(SupportCommands(bot))
    bot.add_cog(SupportEvents(bot))
