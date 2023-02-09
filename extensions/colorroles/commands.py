import string

import discord
from discord import Member, Guild, Role
from discord.errors import Forbidden
from discord.ext import commands
from discord.ext.commands import Context, BucketType, Cog, Group, Command
from typing import Optional, Union


def int_hex(value):
    value = value.lstrip('#')
    if not (len(value) == 6 and all(x in string.hexdigits for x in value)):
        return None

    return int(value, 16)


def croles(roleable: Union[Member, Guild]):
    roles: list[Role] = roleable.roles
    for role in roles:
        color_int = int_hex(role.name.lstrip('cr-'))
        if not (role.name.startswith('cr-') and
                color_int is not None and
                role.color.value == color_int and
                role.permissions.value == 0):
            continue

        yield role


async def remove_croles(ctx: Context, member: Member):
    cleaned = False
    for role in croles(member):
        await member.remove_roles(role)
        await ctx.reply(f'Removed color role `{role.name.lstrip("cr-")}` from {member.mention}.')
        cleaned = True

    if not cleaned:
        await ctx.reply('No color roles removed.')


@commands.group(aliases=['cr', 'crole'])
async def colorrole(ctx: Context):
    if not ctx.invoked_subcommand:
        return


@colorrole.command(name='set', aliases=['add'])
@commands.cooldown(1, 3600, BucketType.member)
async def set_(ctx: Context, value: str):
    guild: Optional[Guild] = ctx.guild
    if not guild:
        return

    value = value.lstrip('#').lower()
    int_value = int_hex(value)
    if int_value is None:
        return

    await ctx.author.remove_roles(*croles(ctx.author))  # Clear previous colors before setting new ones

    correct_role = None
    for role in croles(guild):
        if role.color.value == int_value:
            correct_role = role
            break
    if not correct_role:
        correct_role = await guild.create_role(name=f'cr-{value}', color=discord.Color(int_value))

    if correct_role in ctx.author.roles:
        await ctx.reply(f'You already have corresponding color role of `{value}`.')
        return

    top_pos = ctx.me.roles[-1].position
    await correct_role.edit(position=top_pos - 1)
    await ctx.author.add_roles(correct_role, atomic=True)
    await ctx.reply(f'Successfully added color-role of `{value}` to {ctx.author.mention}.')


@colorrole.command(aliases=['clear', 'reset'])
async def remove(ctx: Context):
    if not ctx.guild:
        return

    await remove_croles(ctx, ctx.author)


@colorrole.command()
@commands.has_permissions(administrator=True)
async def revoke(ctx: Context, member: Optional[Member] = None):
    if member is None:
        await ctx.reply('User not found.')
        return

    await remove_croles(ctx, member)


@colorrole.command(aliases=['clean'])
async def cleanroles(ctx: Context):
    guild: Optional[Guild] = ctx.guild
    if not guild:
        return

    cleaned = False
    for role in croles(guild):
        if not role.members:
            try:
                await role.delete()
                await ctx.reply(f'Deleted unused color role `{role.name.lstrip("cr-")}`.')
                cleaned = True
            except Forbidden:
                await ctx.reply(f'Failed to delete unused color role `{role.name.lstrip("cr-")}`: No Permissions.')

    if not cleaned:
        await ctx.reply('No roles where cleaned; all are used.')


def setup(bot):
    for attr in globals().values():
        if isinstance(attr, (Group, Command)):
            if not attr.parents:
                bot.add_command(attr)
        if isinstance(attr, Cog):
            bot.add_cog(attr)
