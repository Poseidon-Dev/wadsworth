from apps.info.commands import InfoCommands
from apps.info.events import InfoEvents


def setup(bot):
    bot.add_cog(InfoCommands(bot))
    bot.add_cog(InfoEvents(bot))
