async def Main(self, message, command, arguments):
    channel = await self.fetch_channel(self.request_channel)
    guild = message.guild
    wholesome_regular = guild.get_role(645994339599908864)
    french_fry = guild.get_role(647927506984501248)

    queue = self.mongo.db["QueueHistory"].find_one({'$or': [{"Status": "Open"}, {"Status": "Locked"}]})
    if queue:
        await message.channel.send("The Queue is already open!")
    else:
        self.mongo.db["QueueHistory"].insert_one({'QueuePos': 0, 'Queue': [], 'Status': 'Open'})
        await channel.set_permissions(wholesome_regular, read_messages=True)
        await channel.send(f"{french_fry.mention} DMCA Friday song requests are now open!")
        #await channel.send("DMCA Friday song requests are now open! (not mentioning the fries to avoid mass REEEEing)")
