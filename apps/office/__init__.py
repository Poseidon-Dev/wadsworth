from apps.office.commands import OfficeCommands
from apps.office.tasks import OfficeTasks

def setup(bot):
    bot.add_cog(OfficeCommands(bot))
    bot.add_cog(OfficeTasks(bot))
