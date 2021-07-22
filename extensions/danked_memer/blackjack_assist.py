import re

from discord import Message

from botcord.functions import log


def parse_cards(string):
    results = re.findall('(?<=\[`. )(\d|10|J|Q|K|A)(?=`\])', string)
    if not results:
        log(f'Error in bj card parsing: No card found: \n{string}', tag='Error')
        return [], 0, False

    for i in range(len(results)):
        if results[i] in 'JQK':
            results[i] = 10
        elif results[i] == 'A':
            results[i] = 0
        elif results[i] in '2345678910':
            results[i] = int(results[i])
        else:
            log(f'Error in bj card parsing: Unknown card {results[i]}', tag='Error')

    return results


def sum_cards(cards: list):
    total = sum(cards)
    soft = False

    aces = cards.count(0)
    for i in range(aces):
        if total <= 10:
            total += 11
            soft = True
        else:  # total >= 11
            total += 1
    return total, soft


def best_move(player: int, soft: bool, dealer: int) -> str:
    if soft:
        if player >= 19:
            return 's'
        elif player == 18:
            if dealer >= 9:
                return 'h'
            else:  # dealer <= 8
                return 's'
        else:  # player <= 17
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

            user_cards = parse_cards(embed['fields'][0]['value'])
            dealer_cards = parse_cards(embed['fields'][1]['value'])

            user_total, user_soft = sum_cards(user_cards)
            dealer_top = dealer_cards[0]
            await message.channel.send(f'Your total: **`{"A+" + str(user_total - 11) if user_soft else user_total}`** | Dealer top card: **`{dealer_top}`** \nYou should: **{best_move(user_total, user_soft, dealer_top)}**')
