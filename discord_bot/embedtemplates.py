import discord
import datetime


def success(message_title, message_desc):
    embed = discord.Embed(title=str("<:GreenTick:743466991771451394> "+message_title), colour=discord.Colour(0xff2a), description=message_desc,
                          timestamp=datetime.datetime.now())
    return embed


def failure(message_title, message_desc):
    embed = discord.Embed(title=str("<:RedTick:743466992144744468> "+message_title), colour=discord.Colour(0xff001e), description=message_desc,
                          timestamp=datetime.datetime.now())
    return embed


def help(commandlist):
    embed = discord.Embed(title="<:BlueTick:783838821681987594> Command Help", colour=discord.Colour(0x00ffff), description=commandlist,
                          timestamp=datetime.datetime.now())
    embed.set_footer(text="DJ Fry by Ramiris#5376 and kittyn#0015",
                     icon_url="https://cdn.discordapp.com/attachments/743445776491085855/795774307249946644/PFP2.png")
    return embed


def question(question, username):
    embed = discord.Embed(title=str("<:YellowTick:783840786999279619> Question to " + username), colour=discord.Colour(0xffbb00), description=str(question),
                          timestamp=datetime.datetime.now())
    return embed


def dj_update(data):
    embed = discord.Embed(title="Next Up: " + str(data["URI"]), colour=discord.Colour(0xbb00bb),
                          description=str("*Requested by: " + data["User"] + "*"),
                          timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Title:", value=data["Name"], inline=False)
    embed.add_field(name="Played: ", value=data["TimesPlayed"], inline=True)
    embed.add_field(name="Requests: ", value=data["TimesRequested"], inline=True)
    return embed

def pypy_request(data):
    embed = discord.Embed(title="PyPy Song ID:  " + str(data["URI"]), colour=discord.Colour(0xbb00bb),
                          description=str("*Requested by: " + data["User"] + "*"),
                          timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Title:", value=data["Name"], inline=False)
    embed.add_field(name="Played: ", value=data["TimesPlayed"], inline=True)
    embed.add_field(name="Requests: ", value=data["TimesRequested"], inline=True)
    return embed


def song_request(data):
    embed = discord.Embed(title="YouTube URL:  " + str(data["URI"]), colour=discord.Colour(0xbb00bb),
                          description=str("*Requested by: " + data["User"] + "*"),
                          timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Title:", value=data["Name"], inline=False)
    embed.add_field(name="Played: ", value=data["TimesPlayed"], inline=True)
    embed.add_field(name="Requests: ", value=data["TimesRequested"], inline=True)
    return embed


def queue_card(self):
    queue = self.mongo.db["QueueHistory"].find_one({"Status": "Open"})
    print(queue)
    if len(queue["Queue"]) > 20:
        embed = discord.Embed(title="Current Queue", colour=discord.Colour(0x55aaff),
                              description=str("20 / " + str(len(queue["Queue"]))),
                              timestamp=datetime.datetime.utcnow())
        for i in range(len(queue["Queue"])):
            request = self.mongo.db["Requests"].find_one({"_id": queue["Queue"][i]})
            embed.add_field(name=str(str(i) + ". " + request["Name"]), value=str(str(request["TimesRequested"]) + " | " + str(request["TimesPlayed"]) + " | " + str(request["URI"])), inline=False)
    else:
        embed = discord.Embed(title="Current Queue", colour=discord.Colour(0x55aaff),
                              timestamp=datetime.datetime.utcnow())
        for i in range(len(queue["Queue"])):
            request = self.mongo.db["Requests"].find_one({"_id": queue["Queue"][i]})
            embed.add_field(name=str(str(i) + ". " + request["Name"]), value=str(str(request["TimesRequested"]) + " | " + str(request["TimesPlayed"]) + " | " + str(request["URI"])), inline=False)
    embed.set_footer(text="Reqs | Plays | ID/URL")
    return embed
