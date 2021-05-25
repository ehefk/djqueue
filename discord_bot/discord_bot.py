import discord
import asyncio
import queue
from googleapiclient.discovery import build
import importlib
import os
import sys
import traceback
import discord_bot.embedtemplates as embedtemplates
from discord.ext import tasks
import MongoDBInterface
import log_system


class Bot(discord.Client):
    
    cnt = 0
    updated = 1
    Q_LEN = 1

    def __init__(self, GoogleAPIToken, *args, **kwargs):
        asyncio.get_event_loop()
        super().__init__(*args, **kwargs)
        self.YT_API = build('youtube', 'v3', developerKey=GoogleAPIToken)
        self.check_queue.start()
        self.mongo = MongoDBInterface.Main()
        self.queue_channel = 842771764786495498
        self.request_channel = 842771724311330846
        self.logger = log_system.Main()

    #########################################################
    ##
    ##
    ##
    ##
    async def run_file(self, filename, message="", arguments=""):
        command_found = False
        for command_file in os.listdir("discord_bot/commands"):
            if command_file in ["__init__.py", "__pycache__"]:
                continue
            elif command_file[:-3] == filename:
                spec = importlib.util.spec_from_file_location("module.name", str("discord_bot/commands/" + command_file))
                foo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(foo)
                await foo.Main(self, message, filename, arguments)
                command_found = True
        if not command_found:
            await message.channel.send("Command not found!")

    #########################################################
    ##
    ##
    ##
    ##
    async def await_response(self, user):
        def check(message):
            return message.author == user

        try:
            content = await self.wait_for('message', check=check, timeout=100)
        except asyncio.TimeoutError:
            return None
        return content

    async def refresh_queue(self):
        channel = await self.fetch_channel(self.queue_channel)  # Get Log Channel (Temporary)
        queue = self.mongo.db["QueueHistory"].find_one({'$or': [{"Status": "Open"}, {"Status": "Locked"}]})
        if queue:
            if "DiscordMessageID" in queue.keys():
                message = await channel.fetch_message(queue["DiscordMessageID"])
                embed = embedtemplates.queue_card(self)
                await message.edit(content="", embed=embed)
            else:
                embed = embedtemplates.queue_card(self)
                message = await channel.send(content="", embed=embed)
                queue["DiscordMessageID"] = message.id
                self.mongo.db["QueueHistory"].replace_one({'$or': [{"Status": "Open"}, {"Status": "Locked"}]}, queue)

            await message.clear_reactions()
            await message.add_reaction("<:GreyTick:743466991981167138>")
            await message.add_reaction("1️⃣")
            await message.add_reaction("2️⃣")
            await message.add_reaction("3️⃣")
            await message.add_reaction("4️⃣")
            await message.add_reaction("5️⃣")
            return True
        else:
            return False

    async def is_mod(self, userid):
        modlist = [74912563418107904, 110838934644211712]
        if userid in modlist:
            return True
        else:
            return False

    ######################################################
    ##   Background tasks
    ##
    ##
    @tasks.loop(seconds=1) 
    async def check_queue(self):

        dataset = self.mongo.db["Requests"].find({"Status": "Pending"})
        
        for data in dataset:
            await self.wait_until_ready()  # Ensure the Discord Bot is connected (waits if timed out for reconnect)
            spec = importlib.util.spec_from_file_location("module.name", str("discord_bot/handle_queue.py"))
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            message_id = await foo.Main(self, data)
            self.logger.debug("before d update")
            if message_id:
                data["DiscordMessageID"] = message_id
                data["Status"] = "In Queue"
                self.mongo.db["Requests"].replace_one({"URI": data["URI"], "Status": "Pending"}, data)
                self.updated = 1
                await self.refresh_queue()
            else:
                self.logger.error("Message Post Failed - Discord Relay down?")

                #########
        '''##  Table updated if this is true
        ##
        if self.updated:
            self.updated = 0
            self.logger.debug("update")

            ############
            ###  Scan the rows, stop after a few (adjust Q_LEN)
            ###
            dataset = self.mongo.db["Requests"].find({"Status": "Pending"})
            for data in dataset:

                ###########
                ##  Only interested if no message for dj ui
                ##
                ##
                self.logger.debug(data["URI"])
                if "QueueMessageID" not in data.keys():
                    self.logger.debug("No Queue message ID")

                    ##############
                    ##
                    ##  If there's already a few at the top for the dj then we're done
                    ##
                    if self.cnt < self.Q_LEN:
                        self.logger.debug("dj ui setup")

                        spec = importlib.util.spec_from_file_location("module.name", str("discord_bot/handle_ui.py"))
                        foo = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(foo)
                        message_id = await foo.Main(self, data)
                        if message_id:
                            request = self.mongo.db["Requests"].find_one({'$or': [{'Status': 'Pending'}, {'Status': 'On Hold'}, {'Status': 'In Queue'}], "URI": data["URI"]})
                            request["QueueMessageID"] = message_id
                            request["Status"] = "In Queue"
                            self.mongo.db["Requests"].replace_one({'$or': [{'Status': 'Pending'}, {'Status': 'On Hold'}, {'Status': 'In Queue'}], "URI": data["URI"]}, request)
                            if self.Q_LEN < 3:
                                self.Q_LEN = self.Q_LEN + 1

                        self.cnt = self.cnt + 1
                        self.updated = 0
                        #############################
                        ##  could be a problem w logic here
                        ##
                        ##  i think this is right lol
                        ##
                    else:
                        break

                else:
                    self.logger.debug("continue")'''

    #########################################################
    ##
    ##  Runs when bot starts
    ##
    ##
    async def on_ready(self):
        self.logger.info('Logged into discord as "{0.user}"'.format(self))
        activity = discord.Activity(name="music.", type=discord.ActivityType.listening)
        await self.change_presence(activity=activity)
        #self.loop.create_task(await self.check_queue())

    #########################################################
    ##
    ##
    ##
    ##
    async def on_error(self, event, *args, **kwargs):
        type, value, tb = sys.exc_info()
        if event == "on_message":
            try:
                channel = " in #" + args[0].channel.name
            except AttributeError:
                channel = " in private DMs"
            await args[0].channel.send(
                "*An error occured, sorry for the inconvenience. Ramiris has been notified of the error.*")
        else:
            channel = ""
        tbs = "*" + type.__name__ + " exception handled in " + event + channel + " : " + str(
            value) + "*\n\n```\n"
        for string in traceback.format_tb(tb):
            tbs = tbs + string
        tbs = tbs + "```"
        self.logger.exception("*" + type.__name__ + " exception handled in " + event + channel + " : " + str(
            value) + "*\n\n```\n")
        await self.get_user(110838934644211712).send(tbs)

    async def on_message(self, message):
        if message.author.bot or message.channel.type == discord.ChannelType.private or message.channel.type == discord.ChannelType.group:
            return

        if message.content.startswith("!"):
            command = message.content[1:].split(" ")[0]
            arguments = message.content[1:].replace(str(command + " "), "")
            await self.run_file(command, message, arguments)

    #########################################################
    ##
    ##
    ##
    ##
    async def question(self, user, question, channel=None):  # Ask the user a question, specify a channel or it'll DM
        if channel is not None:
            await channel.send(content="", embed=embedtemplates.question(question, user.display_name))
            response = await self.await_response(user)
            if response is None:
                await channel.send(content="", embed=embedtemplates.failure("Response Timed Out",
                                                                            "You took too long to respond!"))
                return None
            return response
        else:
            try:
                await user.send(content="", embed=embedtemplates.question(question, user.display_name))
                response = await self.await_response(user)
                if response is None:
                    await user.send(content="", embed=embedtemplates.failure("Response Timed Out",
                                                                             "You took too long to respond!"))
                    return None
                return response
            except discord.Forbidden:
                self.logger.error(user.name, "Could not be messaged.")
                return None

    #########################################################
    ##
    ##
    ##
    ##
    async def on_raw_reaction_add(self, payload):
        channel = await self.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.fetch_user(payload.user_id)
        emoji = payload.emoji

        if user.bot or message.channel.type == discord.ChannelType.private or message.channel.type == discord.ChannelType.group:
            return

        if message.embeds:
            spec = importlib.util.spec_from_file_location("module.name", str("discord_bot/handle_reactions.py"))
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            self.updated = await foo.Main(self, channel, message, user, emoji)
            if self.updated == 1:
                self.cnt = self.cnt - 1
        
            
