from discord.ext import commands


def guild_owner_or_perms(**perms):
    has_perms = commands.has_permissions(**perms).predicate

    async def check_func(ctx):
        if ctx.guild is None:
            return False
        return ctx.guild.owner_id == ctx.author.id or await has_perms(ctx)

    return commands.check(check_func)


def guild_admin_or_perms(**perms):
    has_perms = commands.has_permissions(**perms).predicate

    async def check_func(ctx):
        if ctx.guild is None:
            return False
        return ctx.message.author.guild_permissions.administrator or await has_perms(ctx)

    return commands.check(check_func)
