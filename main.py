from os import getenv

import discord

import botcord


class SocietyBot(botcord.BotClient):
    def __init__(self, **options):
        super().__init__(**options)


def init():
    CLIENT = SocietyBot(status=discord.Status("online"),
                        activity=discord.Activity(name="a Society | *help", type=3))
    CLIENT.run(getenv("TOKEN"))


init()
