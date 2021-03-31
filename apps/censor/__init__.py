from apps.censor.commands import CensorCommands
from apps.censor.events import CensorEvents

def setup(bot):
    bot.add_cog(CensorCommands(bot))
    bot.add_cog(CensorEvents(bot))