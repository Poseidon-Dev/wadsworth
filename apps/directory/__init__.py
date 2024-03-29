from apps.directory.commands import DirectoryCommands
from apps.directory.events import DirectoryEvents
from apps.directory.tasks import DirectoryTasks

def setup(bot):
    bot.add_cog(DirectoryCommands(bot))
    bot.add_cog(DirectoryEvents(bot))
    bot.add_cog(DirectoryTasks(bot))