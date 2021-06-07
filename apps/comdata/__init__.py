from apps.comdata.commands import ComdataCommands
from apps.comdata.events import ComdataEvents
from apps.comdata.models import ComdataTable

def setup(bot):
    ComdataTable().build()
    bot.add_cog(ComdataCommands(bot))
    bot.add_cog(ComdataEvents(bot))