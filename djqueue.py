# Import Libraries
import asyncio
import threading
import discord_bot.discord_bot as discord_bot
from twitchbot import BaseBot
import sqlite3
import json



#############
## clear requests db - will move this later
##
def botinit():
    con = sqlite3.connect("database.sqlite")
    cursor = con.cursor()
    sqlite_query = """DELETE FROM song_requests;"""
    cursor.execute(sqlite_query)
    sqlite_query = """INSERT INTO song_requests (id, q_length) VALUES (9999, 0)"""
    cursor.execute(sqlite_query)
    con.commit()
    con.close()


def DiscordBot(secrets):
    print("Started Discord Thread")
    discordloop = asyncio.new_event_loop()
    asyncio.set_event_loop(discordloop)
    asyncio.get_event_loop()
    bot = discord_bot.Bot(secrets["GoogleAPIToken"])
    discordloop.create_task(bot.start(secrets["DiscordBotToken"]))
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
    botinit()

    # Open secrets.json file for Tokens
    with open("secrets.json", "r") as file:
        secrets = json.load(file)

    # Setup Thread for Discord Bot
    DiscordThread = threading.Thread(target=DiscordBot, args=(secrets, ))
    DiscordThread.daemon = False
    DiscordThread.start()

    # Setup Thread for Twitch Bot
    TwitchThread = threading.Thread(target=TwitchBot, args=())
    TwitchThread.daemon = False
    TwitchThread.start()

    print("\n\n All Threads Created")
