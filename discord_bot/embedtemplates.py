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
    embed = discord.Embed(title="Next Up: " + data["request"], colour=discord.Colour(0xbb00bb),
                          description=str("*Requested by: " + data["user"] + "*"),
                          timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Title:", value=data["request"], inline=False)
    embed.add_field(name="Played: ", value=data["x_played"], inline=True)
    embed.add_field(name="Requests: ", value=data["x_requested"], inline=True)
    return embed

def pypy_request(data):
    embed = discord.Embed(title="PyPy Song ID:  " + data["uri"], colour=discord.Colour(0xbb00bb),
                          description=str("*Requested by: " + data["user"] + "*"),
                          timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Title:", value=data["request"], inline=False)
    embed.add_field(name="Played: ", value=data["x_played"], inline=True)
    embed.add_field(name="Requests: ", value=data["x_requested"], inline=True)
    return embed


def song_request(data):
    embed = discord.Embed(title="YouTube URL:  " + data["uri"], colour=discord.Colour(0xbb00bb),
                          description=str("*Requested by: " + data["user"] + "*"),
                          timestamp=datetime.datetime.utcnow())
    embed.add_field(name="Title:", value=data["request"], inline=False)
    embed.add_field(name="Played: ", value=data["x_played"], inline=True)
    embed.add_field(name="Requests: ", value=data["x_requested"], inline=True)
    return embed
