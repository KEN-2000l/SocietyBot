from discord.utils import get as _get

from botcord.functions import to_int


async def role(string, guild):
    string = string.strip()
    _role = guild.get_role(to_int(string))
    if _role:
        return _role

    _role = _get(guild.roles, mention=string)
    if _role:
        return _role

    _role = _get(guild.roles, name=string)
    if _role:
        return _role

    return None


async def channel(string, guild):
    string = string.strip()
    _channel = guild.get_channel(to_int(string))
    if _channel:
        return _channel

    _channel = _get(guild.channels, mention=string)
    if _channel:
        return _channel

    _channel = _get(guild.channels, name=string)
    if _channel:
        return _channel

    return None

# End
