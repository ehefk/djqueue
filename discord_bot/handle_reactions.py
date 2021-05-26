import discord


async def Main(self, channel, message, user, emoji):
    Perms = await self.is_dj(user)
    if Perms == False:
        return

    async def complete_request(post):
        Request = self.mongo.db["Requests"].find_one({"DiscordMessageID": post.id})
        if Request:
            Request["Status"] = "Complete"
            self.mongo.db["Requests"].replace_one({"DiscordMessageID": post.id}, Request)
            queue = self.mongo.db["QueueHistory"].find_one({'$or': [{"Status": "Open"}, {"Status": "Locked"}]})
            if Request["_id"] in queue["Queue"]:
                queue["Queue"].remove(Request["_id"])
                self.mongo.db["QueueHistory"].replace_one({'$or': [{"Status": "Open"}, {"Status": "Locked"}]}, queue)
                await self.refresh_queue()

    async def queue_number(num):
        queue = self.mongo.db["QueueHistory"].find_one({'$or': [{"Status": "Open"}, {"Status": "Locked"}]})
        postchannel = await self.fetch_channel(self.secrets["PublicChannel"])
        request = self.mongo.db["Requests"].find_one({"_id": queue["Queue"][num]})
        post = await postchannel.fetch_message(request["DiscordMessageID"])

        embed = post.embeds[0]
        embed.colour = discord.Colour(0xff2a)
        embed.description = embed.description + "\n Request Accepted"
        await post.edit(content="", embed=embed)
        await post.clear_reactions()
        await complete_request(post)

    if "GreenTick" in str(emoji):
        if len(message.embeds) > 0:
            if "PyPy Song ID" in message.embeds[0].title or "YouTube URL" in message.embeds[0].title:
                embed = message.embeds[0]
                embed.colour = discord.Colour(0xff2a)
                embed.description = embed.description + "\n Request Accepted"
                await message.edit(content="", embed=embed)
                await message.clear_reactions()
                await complete_request(message)
                return 1

    elif "RedTick" in str(emoji):
        if len(message.embeds) > 0:
            if "PyPy Song ID" in message.embeds[0].title or "YouTube URL" in message.embeds[0].title:
                embed = message.embeds[0]
                embed.colour = discord.Colour(0xff001e)
                embed.description = embed.description + "\n Request Declined"
                await message.delete()
                await complete_request(message)
                return 1

            elif message.embeds[0].title == "Current Queue":
                await message.delete()

    elif "GreyTick" in str(emoji):
        if len(message.embeds) > 0:
            if message.embeds[0].title == "Current Queue":
                await self.refresh_queue()

    elif "1️⃣" in str(emoji):
        await queue_number(0)

    elif "2️⃣" in str(emoji):
        await queue_number(1)

    elif "3️⃣" in str(emoji):
        await queue_number(2)

    elif "4️⃣" in str(emoji):
        await queue_number(3)

    elif "5️⃣" in str(emoji):
        await queue_number(4)
