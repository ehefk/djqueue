async def Main(self, message, command, arguments):
    channel = await self.fetch_channel(self.secrets["PublicChannel"])
    guild = message.guild

    queue = self.mongo.db["QueueHistory"].find_one({'$or': [{"Status": "Open"}, {"Status": "Locked"}]})
    if queue:
        await message.channel.send("The Queue is already open!")
    else:
        self.mongo.db["QueueHistory"].insert_one({'QueuePos': 0, 'Queue': [], 'Status': 'Open'})
        await channel.send("DMCA Friday song requests are now open!")
        #await channel.send("DMCA Friday song requests are now open! (not mentioning the fries to avoid mass REEEEing)")
