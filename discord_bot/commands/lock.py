async def Main(self, message, command, arguments):
    channel = await self.fetch_channel(self.request_channel)

    queue = self.mongo.db["QueueHistory"].find_one({'Status': "Open"})
    if queue:
        queue["Status"] = "Locked"
        self.mongo.db["QueueHistory"].replace_one({'Status': 'Open'}, queue)
        await channel.send("The DJ has paused any requests!")

    else:
        await channel.send("The Queue is not open!")
