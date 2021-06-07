from apps._template.commands import TemplateCommands
from apps._template.events import TemplateEvents
from apps._template.models import TemplateTable

def setup(bot):
    TemplateTable().build()
    bot.add_cog(TemplateCommands(bot))
    bot.add_cog(TemplateEvents(bot))