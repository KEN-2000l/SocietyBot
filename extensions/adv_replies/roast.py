from random import choice

from discord import Member
from discord.ext.commands import group, Greedy, Context, check_any

from botcord.checks import guild_owner_or_perms, has_global_perms
from botcord.exts.commands import Cog
from botcord.functions import batch


class Roaster(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_init(__file__)

    @property
    def blocked(self) -> list:
        if 'blocked' not in self.config:
            self.config['blocked'] = []
        return self.config['blocked']

    @property
    def roasts(self) -> list:
        if 'roasts' not in self.config:
            self.config['roasts'] = []
        return self.config['roasts']

    def add_roast(self, roast: str):
        self.roasts.append(roast)
        return True

    def remove_roast(self, roast: str):
        try:
            self.roasts.remove(roast)
            return True
        except ValueError:
            return False

    @group(invoke_without_command=True)
    async def roast(self, ctx: Context, members: Greedy[Member] = None):
        """[Toxic] command to roast someone using a random phrase."""
        if not members:
            return
        if not self.roasts:
            await ctx.reply(f'You have no roasts set... \n'
                            f'Add some using the [{ctx.prefix}roast add <roast>] command')
            return
        mentions = ' '.join([i.mention for i in members])
        await ctx.send(f'{mentions} {choice(self.roasts)}')

    @roast.command()
    async def add(self, ctx: Context, *, roast: str):
        """Adds a roast to the random-choice pool"""
        if roast in self.roasts:
            await ctx.reply('This roast already exists')
            return
        if len(roast) > 1000:
            await ctx.reply('Roast is too long!!! (1k char max)')
            return
        if self.add_roast(roast):
            await ctx.reply(f'Successfully added roast: \n```{roast}```')
        else:
            await ctx.reply(f'Failed to add roast: \n```{roast}```')

    @roast.command()
    async def list(self, ctx: Context):
        """Lists all the existing Roasts"""
        if not self.roasts:
            await ctx.reply('No existing roasts.')
            return
        allr = 'All Saved Roasts: \n' + '\n'.join([f'```{i}```' for i in self.roasts])
        for msg in batch(allr):
            await ctx.send(msg)

    @roast.command()
    @check_any(guild_owner_or_perms(administrator=True), has_global_perms(owner=True))
    async def remove(self, ctx: Context, *, roast: str):
        """Removes a matching roast from the pool, Admin-only"""
        if self.remove_roast(roast):
            await ctx.reply(f'Successfully removed roast: \n```{roast}```')
        else:
            await ctx.reply(f'Failed to remove/Did not find roast: \n```{roast}```')

    @roast.command()
    @check_any(guild_owner_or_perms(administrator=True), has_global_perms(owner=True))
    async def reload(self, ctx: Context):
        """Saves/Reloads roasts from disk file-save, Admin-only"""
        self.refresh_config()
        await ctx.reply('Refreshed Roasts from File.')

    @roast.command()
    @check_any(guild_owner_or_perms(administrator=True), has_global_perms(owner=True))
    async def save(self, ctx: Context):
        """Overwrites file data with roasts in memory, Admin-only"""
        self.save_config()
        await ctx.reply('Saved roasts to file')

    @roast.command()
    @check_any(guild_owner_or_perms(administrator=True), has_global_perms(owner=True))
    async def load(self, ctx: Context):
        """Overwrites memory data with roasts in file, Admin-only"""
        self.load_config()
        await ctx.reply('Loaded roasts from file')


def setup(bot):
    bot.add_cog(Roaster(bot))
