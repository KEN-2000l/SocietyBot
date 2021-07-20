import re

from discord import Message

from botcord.functions import log


def find_cards(string: str) -> tuple[list, int, bool]:
    results = re.findall('(?<=\[`. )(\d|10|J|Q|K|A)(?=`\])', string)
    if not results:
        log(f'Error in bj card parsing: No card found: \n{string}', tag='Error')
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
            log(f'Error in bj card parsing: Unknown card {results[i]}', tag='Error')

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
    @bot.listen('on_message')
    async def bj_assist(message: Message):
        if message.author.id == 270904126974590976 and ('Type `h` to **hit**, type `s` to **stand**, or type `e` to **end** the game' in message.content):
            embed = message.embeds[0].to_dict()

            user_value: str = embed['fields'][0]['value']
            memer_value: str = embed['fields'][1]['value']

            _, user_total, user_soft = find_cards(user_value)
            memer_card, _, _ = find_cards(memer_value)
            memer_card = memer_card[0]
            await message.channel.send(f'Your total: **`{"A+" if user_soft else ""}{user_total}`** | Dealer top card: **`{memer_card}`** \nYou should: **{best_move(user_total, user_soft, memer_card)}**')

    @bot.listen('on_message')
    async def job_assist(message: Message):
        # todo
        pass
