import datetime


async def Main(self, message, command, arguments):
    sql = await self.get_sql()
    cursor = sql.cursor()
    cursor.execute("INSERT INTO 'song_requests'('user','request','timestamp','status','discord_message_id') VALUES ('" + message.author.display_name + "','" + message.content.replace('!sr ', '') + "','" + str(datetime.datetime.utcnow()) + "','Pending',NULL);")
    sql.commit()
    sql.close()
    await message.delete()