import discord


async def Main(self, channel, message, user, emoji):
    async def complete_request():
        Request = self.mongo.db["Requests"].find_one({"DiscordMessageID": message.id})
        if Request:
            Request["Status"] = "Complete"
            self.mongo.db["Requests"].replace_one({"DiscordMessageID": message.id}, Request)

    if "GreenTick" in str(emoji):
        embed = message.embeds[0]
        embed.colour = discord.Colour(0xff2a)
        embed.description = embed.description + "\n Request Accepted"
        await message.edit(content="", embed=embed)
        await complete_request()
        return 1

    if "RedTick" in str(emoji):
        embed = message.embeds[0]
        embed.colour = discord.Colour(0xff001e)
        embed.description = embed.description + "\n Request Declined"
        await message.delete()
        await complete_request()
        return 1
