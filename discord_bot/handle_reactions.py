import discord


async def Main(self, channel, message, user, emoji):
    async def complete_request():
        sql = await self.get_sql()
        cursor = sql.cursor()
        cursor.execute('UPDATE "song_requests" SET "status" = "Complete" WHERE "discord_message_id" = ' + str(message.id))
        sql.commit()
        sql.close()

    if "GreenTick" in str(emoji):
        embed = message.embeds[0]
        embed.colour = discord.Colour(0xff2a)
        embed.description = embed.description + "\n Request Accepted"
        print(message.id)
        await message.edit(content="", embed=embed)
        await complete_request()
        return 1

    if "RedTick" in str(emoji):
        embed = message.embeds[0]
        embed.colour = discord.Colour(0xff001e)
        embed.description = embed.description + "\n Request Declined"
        print(message.id)
        await message.delete()
        await complete_request()
        return 1

    if message.embeds[0].fields[0].name == "PyPy ID / Video URL" and "GreenTick" in str(emoji):
        embed = message.embeds[0]
        embed.colour = discord.Colour(0xff2a)
        embed.description = embed.description + "\n Request Accepted"
        await message.edit(content="", embed=embed)
        await complete_request()

    if message.embeds[0].fields[0].name == "PyPy ID / Video URL" and "RedTick" in str(emoji):
        embed = message.embeds[0]
        embed.colour = discord.Colour(0xff001e)
        embed.description = embed.description + "\n Request Declined"
        await message.edit(content="", embed=embed)
        await complete_request()
