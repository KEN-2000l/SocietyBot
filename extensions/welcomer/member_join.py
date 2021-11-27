import datetime
from typing import TYPE_CHECKING

from discord import Member
from discord.ext.commands import Cog

from botcord.functions import log

if TYPE_CHECKING:
    import botcord


class Welcomer(Cog):
    def __init__(self, bot: 'botcord.BotClient'):
        self.bot = bot

    async def get_welcome_channel(self, guild):
        if not (welcome_channel_id := self.bot.ext_guild_config('welcomer', guild)['welcome_channel']):
            log(f'Could not find welcome channel ID in configuration file for guild {guild.id}')
            return None
        if not [welcome_channel := guild.get_channel(welcome_channel_id)]:
            log(f'Could not find welcome channel {welcome_channel_id} in guild {guild.id}', tag='Error')
            return None
        return welcome_channel

    @Cog.listener()
    async def on_member_join(self, member: Member):
        if not (welcome_channel := await self.get_welcome_channel(member.guild)):
            return
        await welcome_channel.send(f'**Fuck off {member.mention}**')

    @Cog.listener()
    async def on_verification_complete(self, member: Member):
        if not (welcome_channel := await self.get_welcome_channel(member.guild)):
            return
        time_difference = datetime.datetime.utcnow() - member.joined_at
        await welcome_channel.send(f'It took `{member.name}` **`{time_difference}`** to press a button.')

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        if not (welcome_channel := await self.get_welcome_channel(member.guild)):
            return
        await welcome_channel.send(f'**`{member.name}#{member.discriminator}`** couldn\'t give three more fucks to stay in society.')


def setup(bot):
    bot.add_cog(Welcomer(bot))
