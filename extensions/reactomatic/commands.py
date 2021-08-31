from discord import Forbidden, NotFound, Message
from discord.utils import get

from botcord import log


async def react(message, reaction):
    try:
        await message.add_reaction(reaction)
    except Forbidden:
        pass
    except NotFound:
        log(f'Reaction {reaction} was not found (in server {message.guild})', tag='Warning')


def setup(bot):
    @bot.listen()
    async def on_message_all(message: Message):
        if message.content.lower().strip() == 'ratio' and message.reference:
            await react(message, '👍')
        if ' vio ' in f' {message.content.lower()} ':
            await react(message, '🔥')
        if ' rishi ' in f' {message.content.lower()} ':
            e = get(bot.emojis, id=833215919571468370)
            await react(message, e)
