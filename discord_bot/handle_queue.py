import discord_bot.embedtemplates as embedtemplates
import discord


async def Main(self, data):

    channel = await self.fetch_channel(self.request_channel)  # Get Log Channel (Temporary)
    print("in main")
    print(data["URI"], str(data["URI"]).isdigit())
    if str(data["URI"]).isdigit():
        print("id int")
        data["Name"] = self.mongo.db["PyPySongList"].find_one({"id": data["URI"]})
        data["Name"] = data["Name"]["title"]
        if data["TimesRequested"] == 1:
            embed = embedtemplates.pypy_request(data)
            print("if py py")
        else:
            try:
                message = await channel.fetch_message(data["DiscordMessageID"])
                embed = embedtemplates.pypy_request(data)
                await message.edit(content="", embed=embed)
                return message.id
            except discord.NotFound:
                embed = embedtemplates.pypy_request(data)

    else:
        print("else a YT link")
        data = await process_youtube(self, data)
        embed = embedtemplates.song_request(data)

    self.mongo.db["Requests"].replace_one({"URI": data["URI"], "Status": "Pending"}, data)
    message = await channel.send(content="", embed=embed)
    await message.add_reaction("<:GreenTick:743466991771451394>")
    await message.add_reaction("<:RedTick:743466992144744468>")
#    message = await post_request(data, channel)
    #print(message.id)
    queue = self.mongo.db["QueueHistory"].find_one({'$or': [{"Status": "Open"}, {"Status": "Locked"}]})
    queue["Queue"].append(data["_id"])
    print(str(data["_id"]) + " added to queue")
    self.mongo.db["QueueHistory"].replace_one({'$or': [{"Status": "Open"}, {"Status": "Locked"}]}, queue)
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
    song = data["URI"]

    request = self.YT_API.videos().list(  # Format Request to YouTube API
        part="snippet,contentDetails,statistics",
        id=song[32:]
    )

    response = request.execute()  # Send Request
    if len(response["items"]) == 0:  # Song not found
        return None
    else:  # Song Found
        data["Name"] = str(response["items"][0]["snippet"]["title"])
        return data
