from apps.support.commands import SupportCommands
from apps.support.events import SupportEvents
from apps.support.models import TicketTable, TicketCommentTable

def setup(bot):
    bot.add_cog(SupportCommands(bot))
    bot.add_cog(SupportEvents(bot))