from apps.censor.commands import CensorCommands

def setup(bot):
    bot.add_cog(CensorCommands(bot))