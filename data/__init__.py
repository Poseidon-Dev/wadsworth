from data.office import OfficeTable
from data.tickets import TicketTable, TicketCommentTable, JitBitTickets, JitBitTicketComments
from data.messages import WadsworthMsg
from data.base import DB

__all__ = ['OfficeTable', 'TicketTable', 'TicketCommentTable', 'DB', 'WadsworthMsg', 'EquipmentsTable', 'EmailTable']

def create_and_fill_tables():
    # Create tables on LocalDB
    print('from here')
    OfficeTable().run()
    TicketTable().run()
    TicketCommentTable().run()

    # Fill Data on init
    JitBitTickets().push_tickets()
    JitBitTicketComments().push_comments()

