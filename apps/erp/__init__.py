from apps.erp.commands import EmployeeCommands
from apps.erp.events import ErpEvents
from apps.erp.tasks import EmployeeTasks
from apps.erp.conn import ErpApiConn
from apps.erp.models import EmployeeTable, EmployeeUpdatesTable, EmployeeLoggerTable, EmployeeDivisionTable, EmployeeMessagesTable

def setup(bot):
    EmployeeTable().build()
    EmployeeUpdatesTable().build()
    EmployeeLoggerTable().build()
    EmployeeDivisionTable().build()
    EmployeeMessagesTable().build()
    # DivisionTable().build()
    # EmployeeTable().build()
    # EmployeeTable().store()
    # EmployeeChangesTable().build()
    # EmployeeLogger().build()
    # Messages().build()
    bot.add_cog(EmployeeCommands(bot))
    bot.add_cog(EmployeeTasks(bot))
    bot.add_cog(ErpEvents(bot))
