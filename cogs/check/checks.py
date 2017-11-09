from discord.ext import commands


def is_owner():
    def is_owner_check(message):
        return message.author.id == '193040053348466690'

    return commands.check(lambda ctx: is_owner_check(ctx.message))