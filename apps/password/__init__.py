from apps.password.commands import PasswordCommands

def setup(bot):
    bot.add_cog(PasswordCommands(bot))