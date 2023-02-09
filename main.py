import time
from os import getenv

import discord

from botcord import BotClient


def init():
    client = BotClient(status=discord.Status("online"),
                       activity=discord.Activity(name="a Society | *help", type=3))
    client.run_threaded(getenv("TOKEN2"))

    # listen for shutdown signal
    try:
        while 1:  # basically wait forever until Interrupt
            time.sleep(69420)
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        client.stop_threaded()


if __name__ == '__main__':
    init()
