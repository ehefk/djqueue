import discord_bot.embedtemplates as embedtemplates


async def Main(self, data):
    new_data = None
    try:
        data["request"] = int(data["request"])  # If is Integer (PyPy ID)
        new_data = await process_pypy(self, data)
    except ValueError:
        if "youtube.com" in data["request"] or "youtu.be" in data["request"]:  # Is a Youtube link
            new_data = await process_youtube(self, data)

    channel = await self.fetch_channel(836759071138119701)  # Get Log Channel (Temporary)
    if new_data is None:
        embed = embedtemplates.unverified_request(data)
        message = await channel.send(content="", embed=embed)
        await message.add_reaction("<:PurpleTick:796199276853723146>")
    else:
        embed = embedtemplates.song_request(new_data)
        message = await channel.send(content="", embed=embed)
        await message.add_reaction("<:GreenTick:743466991771451394>")
        await message.add_reaction("<:RedTick:743466992144744468>")
    return message.id


async def process_pypy(self, data):
    with open("discord_bot/PyPyDance Song List (v2020.12.06).txt", "r", encoding='utf-8') as file:  # get PyPy Sheet
        for line in file.readlines():
            splitline = line.split("\t")  # Split sheet into a table
            if len(splitline) == 1:
                continue
            elif len(splitline) == 3:
                if splitline[1] == str(data["request"]):  # Check ID matches
                    data["song_name"] = splitline[2].replace("\n", "")  # Set Song Name based off Sheet
                    data[
                        "url"] = "https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vQAvsUeoYncuBCN3iJs6RpNFONmUvWumoK4SqKWsJ3svLAY_t0cPvneaGrDQwxzGj4k1RaJ-EhkrRFY/pubhtml#"
                    return data
    return None


async def process_youtube(self, data):
    song = data["request"]

    if "youtu.be" in song:
        song = song.replace("youtu.be/", "www.youtube.com/watch?v=")  # Fixed prefix
        if "?" in song:
            song = song.split("?")[0] + "?" + song.split("?")[1]  # Removes Shortened URL Metadata
    else:
        if "&" in song:
            song = song.split("&")[0]  # Removes Full URL Metadata
    data["request"] = song

    request = self.YT_API.videos().list(  # Format Request to YouTube API
        part="snippet,contentDetails,statistics",
        id=song[32:]
    )
    response = request.execute()  # Send Request
    if len(response["items"]) == 0:  # Song not found
        return None
    else:  # Song Found
        data["song_name"] = response["items"][0]["snippet"]["title"]
        data["url"] = data["request"]
        return data
