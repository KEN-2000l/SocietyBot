from discord.ext import commands
from discord.ext.commands import Group, Command, Cog

import urllib.parse


def search(query):
    return f"http://www.usethefuckinggoogle.com/?q={urllib.parse.quote_plus(query)}"


@commands.command()
async def google(ctx, *, query):
    if not query:
        return
    await ctx.send(search(query))


def setup(bot):
    for attr in globals().values():
        if isinstance(attr, (Group, Command)):
            if not attr.parents:
                bot.add_command(attr)
        if isinstance(attr, Cog):
            bot.add_cog(attr)
