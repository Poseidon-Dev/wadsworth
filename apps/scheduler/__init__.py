from apps.scheduler.commands import SchedulerCommands
from apps.scheduler.events import SchedulerEvents
from apps.scheduler.models import SchedulerTable, SchedulerUserTable
from apps.scheduler.tasks import SchedulerTasks

def setup(bot):
    SchedulerTable().build()
    SchedulerUserTable().build()
    bot.add_cog(SchedulerCommands(bot))
    bot.add_cog(SchedulerEvents(bot))
    bot.add_cog(SchedulerTasks(bot))