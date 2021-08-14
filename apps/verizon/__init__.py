from apps.verizon.events import VerizonEvents

def setup(bot):
    bot.add_cog(VerizonEvents(bot))
