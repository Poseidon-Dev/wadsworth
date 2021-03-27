import discord

class Validators:

    def channel(self, ctx, msg):
        if ctx.message.channel == msg.channel:
            return True
        else:
            return False

    def author(self, ctx, msg):
        if ctx.message.author == msg.author:
            return True
        else:
            return False

    def strict_check(self, msg):
        if ctx.author == msg.author and ctx.channel == msg.channel:
            return True
        else:
            return False

    