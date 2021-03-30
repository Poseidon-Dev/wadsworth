from apps.erps.commands import EmployeeCommands

def setup(bot):
    bot.add_cog(EmployeeCommands(bot))