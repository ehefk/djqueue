import discord


async def Main(self, channel, message, user, emoji):
    async def complete_request():
        Request = self.mongo.db["Requests"].find_one({"DiscordMessageID": message.id})
        if Request:
            Request["Status"] = "Complete"
            self.mongo.db["Requests"].replace_one({"DiscordMessageID": message.id}, Request)
            queue = self.mongo.db["QueueHistory"].find_one({"Status": "Open"})
            if Request["_id"] in queue["Queue"]:
                queue["Queue"].remove(Request["_id"])
                self.mongo.db["QueueHistory"].replace_one({"Status": "Open"}, queue)
                await self.refresh_queue()

    if "GreenTick" in str(emoji):
        if len(message.embeds) > 0:
            if "PyPy Song ID" in message.embeds[0].title or "YouTube URL" in message.embeds[0].title:
                embed = message.embeds[0]
                embed.colour = discord.Colour(0xff2a)
                embed.description = embed.description + "\n Request Accepted"
                await message.edit(content="", embed=embed)
                await complete_request()
                return 1

    if "RedTick" in str(emoji):
        if len(message.embeds) > 0:
            if "PyPy Song ID" in message.embeds[0].title or "YouTube URL" in message.embeds[0].title:
                embed = message.embeds[0]
                embed.colour = discord.Colour(0xff001e)
                embed.description = embed.description + "\n Request Declined"
                await message.delete()
                await complete_request()
                return 1

    if "GreyTick" in str(emoji):
        if len(message.embeds) > 0:
            if message.embeds[0].title == "Current Queue":
                await self.refresh_queue()
