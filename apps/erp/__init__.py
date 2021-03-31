from apps.erp.commands import EmployeeCommands
from apps.erp.migrations import ErpApi

def setup(bot):
    ErpApi().run()
    bot.add_cog(EmployeeCommands(bot))