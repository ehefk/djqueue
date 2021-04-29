import discord
import asyncio
import queue
import datetime
from googleapiclient.discovery import build


class Bot(discord.Client):
    def __init__(self, queues, *args, **kwargs):
        asyncio.get_event_loop()
        super().__init__(*args, **kwargs)
        self.queue = queues[0]
        self.YT_API = build('youtube', 'v3', developerKey="AIzaSyDRB1VWeyZnmnKBYFg9NOg7YNd5Gpy__aY")

    async def process_pypy(self, data):
        with open("PyPyDance Song List (v2020.12.06).txt", "r", encoding='utf-8') as file:  # get PyPy Sheet
            for line in file.readlines():
                splitline = line.split("\t")  # Split sheet into a table
                if len(splitline) == 1:
                    continue
                elif len(splitline) == 3:
                    if splitline[1] == str(data["SongID"]):  # Check ID matches
                        data["SongName"] = splitline[2].replace("\n", "")  # Set Song Name based off Sheet
                        data[
                            "URL"] = "https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vQAvsUeoYncuBCN3iJs6RpNFONmUvWumoK4SqKWsJ3svLAY_t0cPvneaGrDQwxzGj4k1RaJ-EhkrRFY/pubhtml#"
                        return data
        return None

    async def process_youtube(self, data):
        song = data["SongID"]

        if "youtu.be" in song:
            song = song.replace("youtu.be/", "www.youtube.com/watch?v=")  # Fixed prefix
            if "?" in song:
                song = song.split("?")[0] + "?" + song.split("?")[1]  # Removes Shortened URL Metadata
        else:
            if "&" in song:
                song = song.split("&")[0]  # Removes Full URL Metadata
        data["SongID"] = song

        request = self.YT_API.videos().list(  # Format Request to YouTube API
            part="snippet,contentDetails,statistics",
            id=song[32:]
        )
        response = request.execute()  # Send Request
        if len(response["items"]) == 0:  # Song not found
            return None
        else:  # Song Found
            data["SongName"] = response["items"][0]["snippet"]["title"]
            data["URL"] = data["SongID"]
            return data

    async def check_queue(self):
        while True:  # Loops background task
            try:
                data = self.queue.get(block=False)  # Checks queue for new data
            except queue.Empty:  # Queue is Empty
                await asyncio.sleep(1)  # Wait 1 Second then try again
                continue

            await self.wait_until_ready()  # Ensure the Discord Bot is connected (waits if timed out for reconnect)

            if data["Type"] == "SongRequest":  # Handing Song Request Data
                new_data = None
                try:
                    data["SongID"] = int(data["SongID"])  # If is Integer (PyPy ID)
                    new_data = await self.process_pypy(data)
                except ValueError:
                    if "youtube.com" in data["SongID"] or "youtu.be" in data["SongID"]:  # Is a Youtube link
                        new_data = await self.process_youtube(data)

                channel = await self.fetch_channel(836759071138119701)  # Get Log Channel (Temporary)
                if new_data is None:
                    embed = discord.Embed(title="Unverified Request", colour=discord.Colour(0xbb00bb),
                                          description=str("*Requested by: " + data["User"] + "*"),
                                          timestamp=datetime.datetime.utcnow())
                    embed.add_field(name="Message:", value=data["SongID"], inline=False)
                else:
                    embed = discord.Embed(title=new_data["SongName"], colour=discord.Colour(0xffbb00),
                                          url=new_data["URL"], description=str("*Requested by: " + new_data["User"] + "*"),
                                          timestamp=datetime.datetime.utcnow())
                    embed.add_field(name="PyPy ID / Video URL", value=new_data["SongID"], inline=False)
                    embed.add_field(name="Times Played", value="Today: 0\nTotal: 0", inline=False)
                await channel.send(content="", embed=embed)

            await asyncio.sleep(0.2) # Wait a 5th of a second before looping again

    async def on_ready(self):
        print('Logged into discord as "{0.user}"'.format(self))
        activity = discord.Activity(name="music.", type=discord.ActivityType.listening)
        await self.change_presence(activity=activity)
        self.loop.create_task(await self.check_queue())

    async def on_message(self, message):
        if message.content.startswith("!test"):
            self.queue.put({"Type": "SongRequest", "SongID": message.content.strip("!test "), "User": message.author.display_name})
