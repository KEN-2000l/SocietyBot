import string

import discord
from discord.ext import commands
from discord.ext.commands.core import Command
from typing import Optional


def check_hex(value):
    if len(value) == 6:
        if not all(x in string.hexdigits for x in value):
            return None
    else:
        return None

    return int(value, 16)


@commands.group()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def colorrole(ctx):
    if not ctx.invoked_subcommand:
        return


@colorrole.command()
async def remove(ctx, *extra):
    if extra:
        return

    if not ctx.guild:
        return

    roles = ctx.author.roles
    for role in roles:
        if not role.name.startswith('cr-'):
            continue
        color = check_hex(role.name.lstrip('cr-'))
        if not color:
            continue
        if not role.permissions.value == 0:
            continue
        if not role.color.value == color:
            continue

        await ctx.author.remove_roles(role)
        await ctx.reply(f'Removed color role `{role.name.lstrip("cr-")}` from {ctx.author.mention}.')


@colorrole.command(name='set')
async def set_(ctx: discord.ext.commands.Context, value: str, *extra):
    if extra:
        return

    tvalue = value.lower()
    value = check_hex(value)
    if value is None:
        return
    color = discord.Color(value)

    guild: Optional[discord.Guild] = ctx.guild
    if not guild:
        return

    await remove(ctx)

    roles = guild.roles
    for role in roles:
        if not role.name.startswith('cr-'):
            continue
        name = check_hex(role.name.lstrip('cr-'))
        if not name:
            continue
        if color.value == role.color.value == name:
            if not role.permissions.value == 0:
                continue
            top_pos = ctx.me.roles[-1].position
            await role.edit(position=top_pos - 1)
            await ctx.author.add_roles(role, atomic=True)
            await ctx.reply(f'Successfully added color-role of `{tvalue}` to {ctx.author.mention}.')
            return

    crole = await guild.create_role(name=f'cr-{tvalue}', color=color)
    top_pos = ctx.me.roles[-1].position
    await crole.edit(position=top_pos-1)
    await ctx.author.add_roles(crole, atomic=True)
    await ctx.reply(f'Successfully added color-role of `{tvalue}` {ctx.author.mention}')


@colorrole.command()
@commands.has_permissions(administrator=True)
async def revoke(ctx, user: Optional[discord.Member] = None):
    if user is None:
        await ctx.reply('User not found.')
        return
    ctx.author = user
    await remove(ctx)


def setup(bot):
    for attr in globals().values():
        if isinstance(attr, Command):
            bot.add_command(attr)
