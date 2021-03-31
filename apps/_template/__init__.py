from apps._template.commands import TemplateCommands
from apps._tempalte.events import TemplateEvents

def setup(bot):
    bot.add_cog(TemplateCommands(bot))
    bot.add_cog(TemplateEvents(bot))