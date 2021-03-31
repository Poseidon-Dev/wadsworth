from apps.support.commands import SupportCommands
from apps.support.events import SupportEvents
from apps.support.tasks import SupportTasks
from apps.support.models import TicketTable, TicketCommentTable
from apps.support.migrations import JitBitTickets, JitBitTicketComments

def setup(bot):
    # Create Tables
    TicketTable().run()
    TicketCommentTable().run()
    
    # Migrate Data
    JitBitTickets().push_tickets()
    JitBitTicketComments().push_comments()

    # Initialize Bot
    bot.add_cog(SupportCommands(bot))
    bot.add_cog(SupportEvents(bot))
    bot.add_cog(SupportTasks(bot))