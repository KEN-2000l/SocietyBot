from discord import Forbidden


async def react(message, reaction):
    try:
        await message.add_reaction(reaction)
    except Forbidden:
        pass


def setup(bot):
    @bot.listen()
    async def on_message(message):
        if message.content.lower() == 'ratio' and message.reference:
            await react(message, '👍')
