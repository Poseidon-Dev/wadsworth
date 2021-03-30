from apps.office.commands import OfficeCommands

def setup(bot):
    bot.add_cog(OfficeCommands(bot))
