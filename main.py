from os import getenv

import discord

from botcord import BotClient


def init():
    client = BotClient(status=discord.Status("online"),
                       activity=discord.Activity(name="a Society | *help", type=3))
    client.run(getenv("TOKEN2"))


init()
