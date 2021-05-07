from twitchbot import Message, Mod
from urlextract import URLExtract
from urllib.parse import urlparse
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import datetime
import sqlite3
import json


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

    #con = sqlite3.connect("database.sqlite")

    async def get_sql(self):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        sql = sqlite3.connect("database.sqlite")
        sql.row_factory = dict_factory
        return sql

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
        ## reset global id
        self.songID = 0

    #################################################
    ############################################
    ######  Validated user input, process the request
    ######
    ######
    async def procVideo(self, uri, msg: Message):

        sql = await self.get_sql()
        cursor = sql.cursor()


################################
###     9999 = Storage record for current queue length
###
###
        con = sqlite3.connect("database.sqlite")
        cur = con.cursor()
        sqlite_query = """SELECT COUNT(*) FROM song_requests WHERE status = 'In Queue'"""
        cur.execute(sqlite_query)

        qPos = cur.fetchone()[0]

        cur.close()
        con.close()

        print("qPos => " + str(qPos))

        title = ""

        x_requested = 0
        x_played = 0
        

        ##############################################
        ##  if uri is a valid integer, look up the ID and load it
        ##
        if isinstance(uri, int):

            sqlite_query = """SELECT * FROM song_list WHERE id = ?"""
            cursor.execute(sqlite_query, (uri,))

            rec = cursor.fetchone()

            songid = rec["id"]
            title = rec["title"]

            # dupe logic
            sqlite_query = """SELECT * FROM song_requests where song_id = ?"""
            cursor.execute(sqlite_query, (songid,))

            rec = cursor.fetchone()
            print(rec)
            print(uri)
            print("nani")

            if rec:
                x_requested = rec["x_requested"] + 1
                #
                # UPDATE, send msg then return
                sqlite_query = "UPDATE 'song_requests' SET 'status' = 'Pending', 'x_requested' = " + str(x_requested) + " WHERE song_id = " + str(songid)
                cursor.execute(sqlite_query)
                sql.commit()
                sql.close()

                await msg.reply(f'{msg.author}, thanks for the request!  {title}  Has now been requested {x_requested} times and played {x_played} times.')

                return

            else:
                sqlite_query = """INSERT INTO song_requests (user, request, timestamp, status, discord_message_id, uri, x_played, x_requested, song_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""
                cursor.execute(sqlite_query, (msg.author, title, datetime.datetime.now(), "Pending", 1, uri,x_played,x_requested, songid))



            sql.commit()
            cursor.close()


            self.qETA += 120
            

            
        ##############################################
        ##  uri is a YT link, see if it matches JD then load it
        ## 
        else:
            title = ""

        ################################################################
        ################################################################
        ###
        ###     Chatbot will write out song info nodes to the queue
        ###     Discordbot will read them and remove them from the queue
        ###     Queue is a doubly-linked-list to allow random deletions
        ###     Need some async functionality here to communicate w discordbot
        ###
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
        #
        qETA = self.qETA / 60

        if x_requested > 0:
            await msg.reply(f'{msg.author}, thanks for the request! {title} is #{qPos} in queue.  Requested {x_requested} times today.  Join discord to see the queue!')
        else:
            await msg.reply(f'{msg.author}, thanks for the request! {title} is #{qPos} in queue.  Join discord to see the queue!')

        #await msg.reply(f'{msg.author}, thanks for the request! {title} is #{self.qPos} in queue.  The cursorrent ETA is approx {qETA} minutes.  Requested $xTimes today.  Join discord to see the queue!')


