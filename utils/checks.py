from discord.ext import commands


def is_owner():
    def is_owner_check(message):
        return message.author.id == '475703972393648139'

    return commands.check(lambda ctx: is_owner_check(ctx.message))
