async def Main(self, message, command, arguments):
    channel = await self.fetch_channel(self.request_channel)

    queue = self.mongo.db["QueueHistory"].find_one({'$or': [{"Status": "Open"}, {"Status": "Locked"}]})
    if queue:
        queue["Status"] = "Closed"
        self.mongo.db["QueueHistory"].replace_one({'$or': [{"Status": "Open"}, {"Status": "Locked"}]}, queue)
        await channel.send("The Queue is now closed!")

    else:
        await message.channel.send("The Queue is not open!")
