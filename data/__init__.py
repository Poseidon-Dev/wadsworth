from data.office import OfficeTable
from data.tickets import TicketTable, TicketCommentTable, JitBitTickets, JitBitTicketComments
from data.messages import WadsworthMsg
from data.base import DB
# from data.erp import EmployeeTable

__all__ = [
    'OfficeTable',
    'TicketTable',
    'TicketCommentTable',
    'DB',
    'WadsworthMsg',
    'EquipmentsTable',
    'EmailTable',
    'EmployeeTable',
    ]

def create_and_fill_tables():
    # Create tables on LocalDB
    # EmployeeTable().run()
    # EmployeeTable().insert_data()
    OfficeTable().run()

    # Fill Data on init
    TicketTable().run()
    TicketCommentTable().run()
    JitBitTickets().push_tickets()
    JitBitTicketComments().push_comments()

