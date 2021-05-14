import discord
import discord_bot.embedtemplates as embedtemplates


async def Main(self, data):

    channel = await self.fetch_channel(822329304557420565)  # Get UI Channel
#    print("in Hui")
#    print(data["discord_message_id"])
#    print(data["djq_message_id"])
    
    if "QueueMessageID" not in data.keys():
        embed = embedtemplates.dj_update(data)

        message = await channel.send(content="", embed=embed)
        await message.add_reaction("<:GreenTick:743466991771451394>")
        await message.add_reaction("<:RightTick:797270413607567360>")
        await message.add_reaction("<:RedTick:743466992144744468>")
        print(message.id)
        return message.id
    else:
#        print("returning NOONE")
        return None
    
    #print(message.id)
#    message = await post_request(data, channel)

    #return message.id

