from data.identifiers import CategoryTable, DivisionTable, StatusTable
from data.office import OfficeTable
from data.tickets import TicketTable, TicketCommentTable, JitBitTickets, JitBitTicketComments
from data.messages import WadsworthMsg
from data.base import DB
from data.erp import EmployeeTable
from data.assets import AssetTable

import config

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
    if config.TESTING:
        EmployeeTable().run()
    else:
        CategoryTable().run()
        DivisionTable().run()
        StatusTable().run()
        # Create tables on LocalDB
        EmployeeTable().run()
        AssetTable().run()
        EmployeeTable().insert_data()
        OfficeTable().run()

        # Fill Data on init
        TicketTable().run()
        TicketCommentTable().run()
        JitBitTickets().push_tickets()
        JitBitTicketComments().push_comments()
