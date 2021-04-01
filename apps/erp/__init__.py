from apps.erp.commands import EmployeeCommands
from apps.erp.tasks import EmployeeTasks
from apps.erp.migrations import ErpApi
from apps.erp.models import employee_tables_setup

def setup(bot):
    employee_tables_setup()
    # ErpApi().run()
    bot.add_cog(EmployeeCommands(bot))
    # bot.add_cog(EmployeeTasks(bot))