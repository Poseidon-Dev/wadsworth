from apps.scheduler.commands import SchedulerCommands
from apps.scheduler.events import SchedulerEvents
from apps.scheduler.models import SchedulerTable, SchedulerUserTable

def setup(bot):
    SchedulerTable().build()
    SchedulerUserTable().build()
    bot.add_cog(SchedulerCommands(bot))
    bot.add_cog(SchedulerEvents(bot))