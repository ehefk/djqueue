# Import Libraries
import asyncio
import threading
import discord_bot.discord_bot as discord_bot
from twitchbot import BaseBot
import json
import log_system


def DiscordBot(secrets):
    logger.info("Started Discord Thread")
    discordloop = asyncio.new_event_loop()
    asyncio.set_event_loop(discordloop)
    asyncio.get_event_loop()
    bot = discord_bot.Bot(secrets)
    discordloop.create_task(bot.start(secrets["DiscordBotToken"]))
    logger.info("Starting Discord Loop")
    discordloop.run_forever()


def TwitchBot():
    logger.info("Started Twitch Thread")
    relayloop = asyncio.new_event_loop()
    asyncio.set_event_loop(relayloop)
    asyncio.get_event_loop()
    relayloop.create_task(BaseBot().run())
    logger.info("Starting Twitch Loop")
    relayloop.run_forever()


if __name__ == '__main__':
    # Open secrets.json file for Tokens
    with open("secrets.json", "r") as file:
        secrets = json.load(file)

    logger = log_system.Main()

    # Setup Thread for Discord Bot
    DiscordThread = threading.Thread(target=DiscordBot, args=(secrets, ))
    DiscordThread.daemon = False
    DiscordThread.start()

    # Setup Thread for Twitch Bot
    TwitchThread = threading.Thread(target=TwitchBot, args=())
    TwitchThread.daemon = False
    TwitchThread.start()
