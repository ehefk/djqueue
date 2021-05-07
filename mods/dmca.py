from twitchbot import Message, Mod
from urlextract import URLExtract
from urllib.parse import urlparse
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import datetime
import json
from googleapiclient.discovery import build
import MongoDBInterface


####
####    --- use single song_requests table for everything, return sorted db where in_queue
####  
####  - the song_list table updates pending - inqueue - completed
####  - chat => pending,  pending => discord, complete => chat stats, position, eta
####
####    - pending => check for dupe first search for songid, if in song_list increment req count UPDATE  -- also return approx location in queue
####    - inqueue => /////////////////////////////////////////////////////////>>>>>> place in FIFO Q, if front of Q flagged as cancelled, pop & ignore
####    -         => SELECT sorted table WHERE inqueu
####                => update dj UI
####    - complete => decrement counter, reduce ETA by 3 minutes
####   
####    - Discord => X -- flag as cancel UPDATE (completed)  ARROW => Random Queue select one or two with mod TOTALcount
####                => O -- UPDATE (completed)
####    
####    !dmca 555
####
####    !dmca youtube.com/video
####
class DMCA(Mod):
    name = 'dmca'

    #################################
    #####  Globals
    #####
    songdata = {}   ## The full json file data set
    songID = 0      ## Actually not sure why this is needed -- it can't be declared at the top of the async function

    qETA = 0        ## Current Q duration in minutes

    yt_song_id = 2000

    #con = ite3.connect("database.ite")

    #################################
    #####  Runs every time a message is recieved in chat
    #####
    #####    Would like to have this only run on point redeems in future
    #####
    async def on_privmsg_received(self, msg: Message):
        extractor = URLExtract()
        frag = msg.content
        #################################
        ##### Detected a request
        #####
        if '!dance' in frag:
            await msg.reply(f'{msg.author}, the pypy site is temporarily down but you can find the list here: https://bit.ly/3eJly0i')

        if '!reset' in frag and msg.author.lower() == "ramiris_":
            mongo = MongoDBInterface.Main()  # Prepares the database ( NO Cursor required )
            mongo.db["Requests"].delete({'$or': [{'Status': 'Pending'}, {'Status': 'On Hold'}, {'Status': 'In Queue'}]})  # Removes any uncomplete Requests
            
        if '!dmca' in frag:
            ####################################
            #####  Check if it contains a URL
            #####
            uri = extractor.find_urls(frag)

            if uri:

                o = urlparse(uri[0])
                #print(o)

                if 'youtube' in o.netloc or 'youtu.be' in o.netloc:
                    ##################################
                    ### Found a valid YT link, process it
                    ###
                    await self.procVideo(uri[0], msg)
                else:
                    #############################
                    ## Not valid song url
                    await msg.reply(f'{msg.author}, thanks for the request!  We are currrently only accepting youtube links or Just Dance song IDs (preferred).')

            ######################################
            #####  No URL, check for song ID
            #####
            else:
                for word in frag.split():
                    if word.isdigit():
                        self.songID = int(word)
                        songID = self.songID
                        if songID < 1566 and songID > 0:
                            ##################################
                            #####  Found valid song ID, process it
                            #####
                            await self.procVideo(songID, msg)
                            break
                        #############################
                        ## Not valid song ID
                        elif songID > 1566 or songID < 1:
                            await msg.reply(f'{msg.author}, thanks for the request! {songID} is not a valid Just Dance video.  Please check https://pypy.niall.sh/ and try again!')
                            break
                if not self.songID:
                    await msg.reply(f'{msg.author}, not sure what you want to request -- please use a song ID or youtube link!')
        ## reset global id
        self.songID = 0

    #################################################
    ############################################
    ######  Validated user input, process the request
    ######
    ######
    async def procVideo(self, uri, msg: Message):

################################
###     9999 = Storage record for current queue length
###
###
        mongo = MongoDBInterface.Main()  # Prepares the database ( NO Cursor required )
        qPos = str(mongo.db["Requests"].count_documents({'Status': 'In Queue'}))
        print("qPos => " + qPos)

        title = ""

        x_requested = 0
        x_played = 0
        

        ##############################################
        ##  if uri is a valid integer, look up the ID and load it
        ##
        if isinstance(uri, int):

            song = mongo.db["PyPySongList"].find_one({"id": int(uri)})

            request = mongo.db["Requests"].find_one({"URI": int(uri), '$or': [{'Status': 'Pending'}, {'Status': 'On Hold'}, {'Status': 'In Queue'}]})

            if request:
                request["TimesRequested"] += 1
                mongo.db["Requests"].replace_one({"URI": int(uri), '$or': [{'Status': 'Pending'}, {'Status': 'On Hold'}, {'Status': 'In Queue'}]}, request)
                # UPDATE, send msg then return

                await msg.reply(f'{msg.author}, thanks for the request!  {song["title"]}  Has now been requested {request["TimesRequested"]} times and played {request["TimesPlayed"]} times.')

                return

            else:
                if "TimesPlayed" in song.keys():
                    mongo.create_request(msg.author, uri, song["TimesPlayed"])
                else:
                    mongo.create_request(msg.author, uri, 0)

            if "Duration" in song.keys():
                self.qETA += song["Duration"]
            else:
                self.qETA += 120
            
        ##############################################
        ##  uri is a YT link, see if it matches JD then load it
        ## 
        else:
            status = "Pending"
            if "youtu.be" in uri:
                uri = uri.replace("youtu.be/", "www.youtube.com/watch?v=")  # Fixed prefix
                if "?" in uri:
                    uri = uri.split("?")[0] + "?" + uri.split("?")[1]  # Removes Shortened URL Metadata
            else:
                if "&" in uri:
                    uri = uri.split("&")[0]  # Removes Full URL Metadata

            with open("secrets.json", "r") as file:
                secrets = json.load(file)
            YT_API = build('youtube', 'v3', developerKey=secrets["GoogleAPIToken"])

            #  Format Request to YouTube API
            request = YT_API.videos().list(part="snippet,contentDetails,statistics", id=uri[32:])
            response = request.execute()  # Send Request
            if len(response["items"]) == 0:  # Song not found
                await msg.reply(f'{msg.author}, thanks for the request!  We are currrently only accepting youtube links or Just Dance song IDs (preferred).')
                return
            else:  # Song Found
                title = response["items"][0]["snippet"]["title"]
                length = response["items"][0]["contentDetails"]["duration"]  # Length in format "PT##M##S"
                length = int(length.split("M")[0][2:])*60 + int(length.split("M")[1][:-1])  # Length in Seconds
                song = mongo.db["SongHistory"].find_one({"URI": int(uri)})

                ################################################################
                ################################################################
                ###
                ###     Chatbot will write out song info nodes to the queue
                ###     Discordbot will read them and remove them from the queue
                ###     Queue is a doubly-linked-list to allow random deletions
                ###     Need some async functionality here to communicate w discordbot
                ###
                ###
                if "Dance" not in title:
                    await msg.reply(
                        f'{msg.author}, thanks for the request!  We are currrently only accepting youtube links that contain Dance Instructional Videos.')
                    return
                ##############################################
                ##  check if song already played, if so, increment request count and inform requester
                ##

                ##############################################
                ##  check if song already requested but not yet played, if so, increment request count
                ##   - check if requester is in last 5 requests or requesting fitness Marshall Songs
                ##      - add song to end of queue if not
                ##      - add marshall requests to marshall queue
                ##      - else add song to randomizer queue
                ##
                if "Marshall" in title:
                    Search = mongo.db["Requests"].count_documents({'$or': [{'Status': 'Pending'}, {'Status': 'On Hold'}, {'Status': 'In Queue'}], 'Tags': {'$in': ['Marshall']}})
                    if len(Search) >= 2:

                        if song:
                            mongo.create_request(msg.author, uri, song["TimesPlayed"], status="On Hold")
                        else:
                            mongo.create_request(msg.author, uri, 0, status="On Hold")

                if song:
                    mongo.create_request(msg.author, uri, song["TimesPlayed"])
                else:
                    mongo.create_request(msg.author, uri, 0)

                self.qETA += length

        ##############################################
        ##  
        #
        qETA = self.qETA / 60

        if x_requested > 0:
            await msg.reply(f'{msg.author}, thanks for the request! {title} is #{qPos} in queue.  Requested {x_requested} times today.  Join discord to see the queue!')
        else:
            await msg.reply(f'{msg.author}, thanks for the request! {title} is #{qPos} in queue.  Join discord to see the queue!')

        #await msg.reply(f'{msg.author}, thanks for the request! {title} is #{self.qPos} in queue.  The cursorrent ETA is approx {qETA} minutes.  Requested $xTimes today.  Join discord to see the queue!')


