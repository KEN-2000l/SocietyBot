from discord.ext import commands
from discord.ext.commands.core import Cog, Group, Command
from discord import Webhook, User
from typing import List, Optional


@commands.command()
async def send(ctx, *, text=None):
    if text:
        await ctx.send(text)


@commands.command()
async def resend(ctx, *, text=None):
    await sendas(ctx, user=ctx.author, text=text)


@commands.command()
async def sendas(ctx, user: Optional[User] = None, *, text=None):
    if (user is None) or (text is None):
        return
    attachments = []
    if ctx.message.attachments:
        attachments = [await atm.to_file() for atm in ctx.message.attachments]

    hooks: Optional[List[Webhook]] = await ctx.channel.webhooks()
    for hook in hooks:
        if not hook.token:
            print('asdf')
            hooks.remove(hook)

    if hooks:
        hook = hooks[0]
    else:
        hook: Webhook = await ctx.channel.create_webhook(name='MessageHook')

    print(hook.token)
    await hook.send(content=text, username=user.name, avatar_url=user.avatar_url, files=attachments)


@commands.command()
async def cleanhooks(ctx, *args):
    if args:
        return
    if not ctx.guild:
        return
    hooks: Optional[List[Webhook]] = await ctx.guild.webhooks()
    if not hooks:
        await ctx.reply('No hooks cleaned.')
        return
    deleted = 0
    for hook in hooks:
        if hook.name == 'MessageHook':
            await hook.delete()
            deleted += 1
    await ctx.reply(f'Deleted {deleted} hook{"s" if deleted > 1 else ""}.')


def setup(bot):
    for attr in globals().values():
        if isinstance(attr, (Group, Command)):
            if not attr.parents:
                bot.add_command(attr)
        if isinstance(attr, Cog):
            bot.add_cog(attr)
