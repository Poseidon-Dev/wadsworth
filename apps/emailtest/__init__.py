from apps.emailtest.tasks import EmailtestTasks


def setup(bot):
    bot.add_cog(EmailtestTasks(bot))
