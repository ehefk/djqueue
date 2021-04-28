# Import Libraries
import asyncio
import queue
import threading
import discord_bot
from twitchbot import BaseBot


def DiscordBot(queues):
    print("Started Discord Thread")
    discordloop = asyncio.new_event_loop()
    asyncio.set_event_loop(discordloop)
    asyncio.get_event_loop()
    bot = discord_bot.Bot(queues)
    discordloop.create_task(bot.start("ODIyMzE3NzU5MzIzOTYzNDIz.YFQhFw.m080OUzrbbwDaYvHrnxiAD3K6SU"))
    print("Starting Discord Loop")
    discordloop.run_forever()


def TwitchBot(queues):
    print("Started Twitch Thread")
    relayloop = asyncio.new_event_loop()
    asyncio.set_event_loop(relayloop)
    asyncio.get_event_loop()
    relayloop.create_task(BaseBot().run())
    print("Starting Twitch Loop")
    relayloop.run_forever()


if __name__ == '__main__':
    # Create Communication Queues
    DiscordQueue = queue.Queue()
    TwitchQueue = queue.Queue()

    DiscordThread = threading.Thread(target=DiscordBot, args=((DiscordQueue, TwitchQueue),))
    DiscordThread.daemon = False
    DiscordThread.start()

    TwitchThread = threading.Thread(target=TwitchBot, args=((DiscordQueue, TwitchQueue),))
    TwitchThread.daemon = False
    TwitchThread.start()

    print("\n\n All Threads Created")
