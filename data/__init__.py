from data.office import OfficeTable
from data.tickets import TicketTable, TicketCommentTable, JitBitTickets, JitBitTicketComments
from data.messages import WadsworthMsg
from data.base import DB

__all__ = ['OfficeTable', 'TicketTable', 'TicketCommentTable', 'DB', 'WadsworthMsg']


def create_and_fill_tables():
    # Create tables on LocalDB
    OfficeTable().run()
    # TicketTable().run()
    # TicketCommentTable().run()

    # Fill Data on init
    # JitBitTickets().push_tickets()
    # JitBitTicketComments().push_comments()

    complete = 'Initial Connection to JitBit API Complete'
    return complete

create_and_fill_tables()