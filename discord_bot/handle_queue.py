import discord_bot.embedtemplates as embedtemplates


async def Main(self, data):

    channel = await self.fetch_channel(836759071138119701)  # Get Log Channel (Temporary)
    print("in main")

    if data["uri"].isnumeric:
        print("id int")
        if data["x_requested"] == 0:
            embed = embedtemplates.pypy_request(data)
            print("if py py")
        else:
            message = await channel.fetch_message(data["discord_message_id"])
            embed = embedtemplates.pypy_request(data)
            await message.edit(content="", embed=embed)
            return message.id
    else:
        print("else")
        embed = embedtemplates.song_request(data)

    message = await channel.send(content="", embed=embed)
    await message.add_reaction("<:GreenTick:743466991771451394>")
    await message.add_reaction("<:RightTick:797270413607567360>")
    await message.add_reaction("<:RedTick:743466992144744468>")
#    message = await post_request(data, channel)
    #print(message.id)
    return message.id


#async def post_request(data, channel):
#    if isinstance(data["id"], int):
#        if data["x_requested"] == 1:
#            embed = embedtemplates.pypy_request(data)
#        else:
#            message = await channel.fetch_message(data["discord_message_id"])
#            embed = embedtemplates.pypy_request(data)
#            await message.edit(content="", embed=embed)
#            return message.id
#    else:
#        embed = embedtemplates.song_request(data)
#
#    message = await channel.send(content="", embed=embed)
#    await message.add_reaction("<:GreenTick:743466991771451394>")
#    await message.add_reaction("<:RightTick:797270413607567360>")
#    await message.add_reaction("<:RedTick:743466992144744468>")
#
#    return message
#
#
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
