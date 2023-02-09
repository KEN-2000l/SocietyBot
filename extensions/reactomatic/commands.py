from typing import Union

from discord import Forbidden, NotFound, Message, Emoji
from discord.utils import get

from botcord import log, contain_word


async def setup(bot):
    async def react(message: Message, reaction: Union[int, str, Emoji]):
        try:
            if isinstance(reaction, int):
                reaction = get(bot.emojis, id=reaction)
            await message.add_reaction(reaction)
        except Forbidden:
            pass
        except NotFound:
            log(f'Reaction {reaction} was not found (in server {message.guild})', tag='Warning')
        except TypeError:
            log(f'Tried to react with Invalid emoji: {reaction}', tag='Warning')

    @bot.listen()
    async def on_message_all(message: Message):
        if message.content.lower().strip() == 'ratio' and message.reference:
            await react(message, '👍')
        if contain_word(message, ['vio', 'violation']):
            await react(message, '🔥')
        if contain_word(message, 'rishi'):
            await react(message, 833215919571468370)
        if contain_word(message, 'whenchamp'):
            await react(message, 885184602526863380)
