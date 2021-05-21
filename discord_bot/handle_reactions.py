import discord


async def Main(self, channel, message, user, emoji):
    Perms = await self.is_mod(user.id)
    if Perms == False:
        return

    async def complete_request():
        Request = self.mongo.db["Requests"].find_one({"DiscordMessageID": message.id})
        if Request:
            Request["Status"] = "Complete"
            self.mongo.db["Requests"].replace_one({"DiscordMessageID": message.id}, Request)
            queue = self.mongo.db["QueueHistory"].find_one({'$or': [{"Status": "Open"}, {"Status": "Locked"}]})
            if Request["_id"] in queue["Queue"]:
                queue["Queue"].remove(Request["_id"])
                self.mongo.db["QueueHistory"].replace_one({'$or': [{"Status": "Open"}, {"Status": "Locked"}]}, queue)
                await self.refresh_queue()

    if "GreenTick" in str(emoji):
        if len(message.embeds) > 0:
            if "PyPy Song ID" in message.embeds[0].title or "YouTube URL" in message.embeds[0].title and await self.is_mod(user.id):
                embed = message.embeds[0]
                embed.colour = discord.Colour(0xff2a)
                embed.description = embed.description + "\n Request Accepted"
                await message.edit(content="", embed=embed)
                await message.clear_reactions()
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

            elif message.embeds[0].title == "Current Queue" and await self.is_mod(user.id):
                await message.delete()

    if "GreyTick" in str(emoji):
        if len(message.embeds) > 0:
            if message.embeds[0].title == "Current Queue":
                await self.refresh_queue()
