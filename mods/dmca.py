from twitchbot import Message, Mod
from urlextract import URLExtract
from urllib.parse import urlparse
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import json

class DMCA(Mod):
    name = 'dmca'

    #################################
    #####  Globals
    #####
    songdata = {}
    songID = 0

    #################################
    #####  Class constructor, read json database - since only needed by chat ingest this is fine
    #####
    def __init__(self):
        with open('songdata.json') as json_file:
            self.songdata = json.load(json_file)

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
                    await msg.reply(f'{msg.author}, thanks for the request!  We are currently only accepting youtube links or Just Dance song IDs (preferred).')

            ######################################
            #####  No URL, check for song ID
            #####
            else:
                for word in frag.split():
                    if word.isdigit():
                        self.songID = int(word)
                        songID = self.songID
                        if songID < 1600 and songID > 0:
                            ##################################
                            #####  Found valid song ID, process it
                            #####
                            await self.procVideo(songID, msg)
                            break
                        #############################
                        ## Not valid song ID
                        elif songID > 1600 or songID < 1:
                            await msg.reply(f'{msg.author}, thanks for the request! {songID} is not a valid Just Dance video.  Please check https://pypy.niall.sh/ and try again!')
                            break
                if not self.songID:
                    await msg.reply(f'{msg.author}, not sure what you want to request -- please use a song ID or youtube link!')

    #################################################
    ############################################
    ######  Validated user input, process the request
    ######
    ######
    async def procVideo(self, uri, msg: Message):
        print(self.songdata)
        title = ""

        ##############################################
        ##  if uri is a valid integer, look up the ID and load it
        ##
        if isinstance(uri, int):
            title = "JustD ID"

            
        ##############################################
        ##  uri is a YT link, see if it matches JD then load it
        ## 
        else:
            title = "JSON Fetch"

        ################################################################
        ################################################################
        ###
        ###     Chatbot will write out song info nodes to the queue
        ###     Discordbot will read them and remove them from the queue
        ###     Queue is a doubly-linked-list to allow random deletions
        ###     Need some inter-thread function here
        ###

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

        ##############################################
        ##  
        ##

        await msg.reply(f'{msg.author}, thanks for the request! {title} is now $qPos in queue.  The current ETA is approx. $qETA minutes.  Requested $xTimes today.  Join discord to see the queue!')



    #####################################################
    ##############################################
    #####  Queue / Linked-list
    #####
    #####
