# Import Libraries
import asyncio
import threading
import discord_bot.discord_bot as discord_bot
from twitchbot import BaseBot


def DiscordBot():
    print("Started Discord Thread")
    discordloop = asyncio.new_event_loop()
    asyncio.set_event_loop(discordloop)
    asyncio.get_event_loop()
    bot = discord_bot.Bot()
    discordloop.create_task(bot.start("ODIyMzE3NzU5MzIzOTYzNDIz.YFQhFw.eaX6iFiCkic_cNiBSikvmLj7l5U"))
    print("Starting Discord Loop")
    discordloop.run_forever()


def TwitchBot():
    print("Started Twitch Thread")
    relayloop = asyncio.new_event_loop()
    asyncio.set_event_loop(relayloop)
    asyncio.get_event_loop()
    relayloop.create_task(BaseBot().run())
    print("Starting Twitch Loop")
    relayloop.run_forever()


if __name__ == '__main__':
    # Create Communication Queues
    DiscordThread = threading.Thread(target=DiscordBot, args=())
    DiscordThread.daemon = False
    DiscordThread.start()

    TwitchThread = threading.Thread(target=TwitchBot, args=())
    TwitchThread.daemon = False
    TwitchThread.start()

    print("\n\n All Threads Created")
