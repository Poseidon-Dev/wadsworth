from apps.google.events import GoogleEvents
from apps.google.models import GoogleTable
from apps.google.tasks import GoogleTasks


def setup(bot):
    GoogleTable().build()
    bot.add_cog(GoogleEvents(bot))
    bot.add_cog(GoogleTasks(bot))