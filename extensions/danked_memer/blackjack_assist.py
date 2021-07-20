import re
from typing import Optional, Any

from discord.ext import commands
from discord.ext.commands import Group, Command, Cog
from discord import Message


def find_cards(string: str) -> tuple[list, int, bool]:
    results = re.findall('(?<=\[`. )(\d|10|J|Q|K|A)(?=`\])', string)
    if not results:
        print('error in bj card parsing')
        return [], 0, False

    soft = False
    total = 0
    for i in range(len(results)):
        result = results[i]
        if result in 'JQK':
            results[i] = 10
            total += 10
        elif result == 'A':
            results[i] = 11
            soft = True
        elif result in '2345678910':
            results[i] = int(results[i])
            total += int(results[i])
        else:
            print('error in bj card parsing')

    return results, total, soft


def best_move(player: int, soft: bool, dealer: int) -> str:
    if soft:
        if player >= 8:
            return 's'
        elif player == 7:
            if dealer >= 9:
                return 'h'
            else:  # dealer <= 8
                return 's'
        else:  # player <= 6
            return 'h'
    else:  # hard
        if player >= 17:
            return 's'
        elif 13 <= player <= 16:
            if dealer >= 7:
                return 'h'
            else:  # dealer <= 6
                return 's'
        elif player == 12:
            if dealer <= 3:
                return 'h'
            elif 4 <= dealer <= 6:
                return 's'
            else:  # dealer >= 7
                return 'h'
        else:  # player <= 11
            return 'h'


def setup(bot):
    for attr in globals().values():
        if isinstance(attr, (Group, Command)):
            if not attr.parents:
                bot.add_command(attr)
        if isinstance(attr, Cog):
            bot.add_cog(attr)

    @bot.listen()
    async def on_message(message: Message):
        if message.author.id == 270904126974590976 and ('Type `h` to **hit**, type `s` to **stand**, or type `e` to **end** the game' in message.content):
            embed = message.embeds[0].to_dict()

            user_value: str = embed['fields'][0]['value']
            memer_value: str = embed['fields'][1]['value']

            _, user_total, user_soft = find_cards(user_value)
            memer_card, _, _ = find_cards(memer_value)
            memer_card = memer_card[0]
            await message.channel.send(f'Your total: **`{"A+" if user_soft else ""}{user_total}`** | Dealer top card: **`{memer_card}`** \nYou should: **{best_move(user_total, user_soft, memer_card)}**')

# **You tied with your opponent!**
# Your wallet hasn't changed! You have **⏣ 27,554** still.
# KEN_2000
# Cards - **[`♥ 4`](https://google.com)  [`♣ 4`](https://google.com)  [`♣ 5`](https://google.com)  [`♥ 5`](https://google.com)**
# Total - `18`
# Dank Memer
# Cards - **[`♠ 8`](https://google.com)  [`♦ Q`](https://google.com)**
# Total - `18`
# Percent Won: 0%
