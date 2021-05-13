from apps.erp.commands import EmployeeCommands
from apps.erp.events import ErpEvents
from apps.erp.tasks import EmployeeTasks
from apps.erp.migrations import ErpApiConn
from apps.erp.models import DivisionTable, EmployeeTable, EmployeeChangesTable, EmployeeLogger, Messages

def setup(bot):
    DivisionTable()
    EmployeeTable()
    EmployeeChangesTable()
    EmployeeLogger()
    Messages()
    # EmployeeFuturesTable().run()
    # ErpApi().run()
    # ErpApiFutures().run()
    bot.add_cog(EmployeeCommands(bot))
    bot.add_cog(EmployeeTasks(bot))
    bot.add_cog(ErpEvents(bot))
