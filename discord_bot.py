import discord
import asyncio
import queue


class Bot(discord.Client):
    def __init__(self, queues, *args, **kwargs):
        asyncio.get_event_loop()
        super().__init__(*args, **kwargs)
        self.queue = queues[0]

    async def check_queue(self):
        while True:
            try:
                data = self.queue.get(block=False)
            except queue.Empty:
                await asyncio.sleep(1)
                continue
            await self.wait_until_ready()
            if data["Type"] == "SongRequest":
                print(str(data))
                channel = await self.fetch_channel(836759071138119701)
                await channel.send(str(data))
            await asyncio.sleep(0.2)

    async def on_ready(self):
        print('Logged into discord as "{0.user}"'.format(self))
        activity = discord.Activity(name="to music.", type=discord.ActivityType.listening)
        await self.change_presence(activity=activity)
        self.loop.create_task(await self.check_queue())

    async def on_message(self, message):
        if message.content.startswith("!test"):
            self.queue.put({"Type": "SongRequest", "SongID": 0, "SongName": "Ra Ra Rasputin"})
