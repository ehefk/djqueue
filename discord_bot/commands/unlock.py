async def Main(self, message, command, arguments):
    channel = await self.fetch_channel(self.secrets["PublicChannel"])

    queue = self.mongo.db["QueueHistory"].find_one({'Status': "Locked"})
    if queue:
        queue["Status"] = "Open"
        self.mongo.db["QueueHistory"].replace_one({'Status': 'Locked'}, queue)
        await channel.send("The DJ has resumed requests!")

    else:
        await channel.send("The Queue is not Locked!")
