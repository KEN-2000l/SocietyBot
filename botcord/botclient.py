from sys import __stdout__
from typing import Iterable
import importlib
import os

import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound, DisabledCommand, CheckFailure, CommandOnCooldown, UserInputError

from .configs import load_configs
from .functions import *
from .utils.extensions import get_all_extensions_from


class BotClient(commands.Bot):
    def __init__(self, **options):
        global_configs, guild_configs, guild_prefixes = load_configs()
        prefix_check = BotClient.mentioned_or_in_prefix if global_configs['bot']['reply_to_mentions'] else BotClient.in_prefix
        super().__init__(**options,
                         command_prefix=prefix_check,
                         max_messages=global_configs['bot']['message_cache'],
                         intents=discord.Intents.all())
        self.last_message = None
        self.configs = global_configs
        self.guild_configs = guild_configs if isinstance(guild_configs, Iterable) else tuple()
        self.prefix = global_configs['bot']['prefix']
        self.guild_prefixes = guild_prefixes if isinstance(guild_prefixes, Iterable) else tuple()
        exts = importlib.import_module(self.configs['bot']['extension_name'], os.getcwd())
        self.load_extensions(exts)

    @staticmethod
    async def in_prefix(bot, message):
        guild_id = getattr(message.guild, 'id', None)
        if (guild_id is not None) and (guild_id in bot.guild_prefixes):
            if message.content.startswith(bot.guild_prefixes[guild_id]):
                return bot.guild_prefixes[guild_id]
        return bot.prefix

    @staticmethod
    async def mentioned_or_in_prefix(bot, message):
        return commands.when_mentioned_or(*await BotClient.in_prefix(bot, message))(bot, message)

    async def logm(self, message, tag="Main", sep="\n", channel=None):
        __stdout__.write(f"[{current_time()}] [{tag}]: {message}" + sep)
        if not channel:
            channel = self.last_message.channel
        await channel.send(message)

    async def on_ready(self):
        log(f"User Logged in as <{self.user}>", tag="Connection")

    async def on_connect(self):
        log(f"Discord Connection Established. <{self.user}>", tag="Connection")

    async def on_disconnect(self):
        log(f"Discord Connection Lost. <{self.user}>", tag="Connection")

    async def on_resume(self):
        log(f"Discord Connection Resumed. <{self.user}>", tag="Connection")

    async def on_typing(self, channel, user, when):
        pass

    async def on_message(self, message):
        await super().on_message(message)

    async def on_message_delete(self, message):
        pass

    async def on_message_edit(self, before, after):
        pass

    async def on_reaction_add(self, reaction, user):
        pass

    async def on_reaction_remove(self, reaction, user):
        pass

    async def on_reaction_clear(self, message, reactions):
        pass

    async def on_reaction_clear_emoji(self, reaction):
        pass

    async def on_private_channel_create(self, channel):
        await self.on_guild_channel_create(channel)

    async def on_private_channel_delete(self, channel):
        await self.on_guild_channel_delete(channel)

    async def on_private_channel_update(self, before, after):
        await self.on_guild_channel_update(before, after)

    async def on_private_channel_pins_update(self, channel, last_pin):
        await self.on_guild_channel_pins_update(channel, last_pin)

    async def on_guild_channel_create(self, channel):
        pass

    async def on_guild_channel_delete(self, channel):
        pass

    async def on_guild_channel_update(self, before, after):
        pass

    async def on_guild_channel_pins_update(self, channel, last_ping):
        pass

    async def on_guild_integrations_update(self, guild):
        pass

    async def on_webhooks_update(self, channel):
        pass

    async def on_member_join(self, member):
        pass

    async def on_member_remove(self, member):
        pass

    async def on_member_update(self, before, after):
        pass

    async def on_user_update(self, before, after):
        pass

    async def on_guild_join(self, guild):
        pass

    async def on_guild_remove(self, guild):
        pass

    async def on_guild_update(self, before, after):
        pass

    async def on_guild_role_create(self, role):
        pass

    async def on_guild_role_delete(self, role):
        pass

    async def on_guild_role_update(self, before, after):
        pass

    async def on_guild_emojis_update(self, before, after):
        pass

    async def on_guild_available(self, guild):
        pass

    async def on_guild_unavailable(self, guild):
        pass

    async def on_voice_state_update(self, member, before, after):
        pass

    async def on_member_ban(self, guild, user):
        pass

    async def on_member_unban(self, guild, user):
        pass

    async def on_invite_create(self, invite):
        pass

    async def on_invite_delete(self, invite):
        pass

    async def on_group_join(self, channel, user):
        pass

    async def on_group_remove(self, channe, user):
        pass

    async def on_relationship_add(self, relationship):
        pass

    async def on_relationship_remove(self, relationship):
        pass

    async def on_relationship_update(self, before, after):
        pass

    async def on_command(self, context):
        pass

    async def on_command_error(self, context, exception):
        if isinstance(exception, (CommandNotFound, DisabledCommand, CheckFailure)) or (context.command is None):
            return
        if isinstance(exception, CommandOnCooldown):
            await context.reply('Command on cooldown you fucktard.')
            return
        if isinstance(exception, UserInputError):
            await context.reply('Invalid inputs.')
            return

        await super().on_command_error(context, exception)

    async def on_command_completion(self, context):
        pass

    async def load_commands(self):
        pass

    def load_extensions(self, package):
        extensions = get_all_extensions_from(package)
        for extension in extensions:
            self.load_extension(extension)

# End
