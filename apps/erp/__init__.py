from apps.erp.commands import EmployeeCommands
from apps.erp.migrations import ErpApi
from apps.erp.models import employee_tables_setup

def setup(bot):
    employee_tables_setup()
    ErpApi().run()
    bot.add_cog(EmployeeCommands(bot))