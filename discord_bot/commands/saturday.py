async def Main(self, message, command, arguments):
    channel = await self.fetch_channel(self.request_channel)
    guild = message.guild
    wholesome_regular = guild.get_role(645994339599908864)

    queue = self.mongo.db["QueueHistory"].find_one({'$or': [{"Status": "Open"}, {"Status": "Locked"}]})
    if queue:
        queue["Status"] = "Closed"
        self.mongo.db["QueueHistory"].replace_one({'$or': [{"Status": "Open"}, {"Status": "Locked"}]}, queue)
        await channel.set_permissions(wholesome_regular, read_messages=False)
        await channel.send("As the sun rises, all good things must come to an end... The Queue is now closed!")

    else:
        await message.channel.send("The Queue is not open!")
