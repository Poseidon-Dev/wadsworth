from apps.erp.commands import EmployeeCommands
from apps.erp.events import ErpEvents
from apps.erp.tasks import EmployeeTasks
from apps.erp.migrations import ErpApi
from apps.erp.models import DivisionTable, EmployeeTable

def setup(bot):
    DivisionTable().run()
    EmployeeTable().run()
    ErpApi().run()
    bot.add_cog(EmployeeCommands(bot))
    bot.add_cog(EmployeeTasks(bot))
    bot.add_cog(ErpEvents(bot))
