# DJ Fry
A DJ Queue bot for Just Dance Streams using Discord and Twitch.

*Originaly called: djqueue*

##Modules

- ***PythonTwitchBotFramework*** - Twitch IRC & PubSub Client  
  - https://github.com/sharkbound/PythonTwitchBotFramework
  - Might be able to get away from this in a future iteration
  - Need to setup pubsub if want to handle point requests instead of chat messages; would be more efficient
  - Potenitally using a custom modification of library for uses?

- ***DiscordPy*** - Discord Bot Client
  - https://discordpy.readthedocs.io/en/stable/ 
  - Runs the Discord Bot Client for interfaces.
  - Currently very for purpose, looking to make a framework.
  
- ***GoogleAPIPythonClient*** - Google API Interface, for access to YouTubeAPI
  - https://developers.google.com/youtube/v3/docs/search/list
  - Used to get video information straight from the YouTube database.
  - Limited to 20,000 requests per day.
  
- ***PyMongo*** - MongoDB Interface
  - https://pymongo.readthedocs.io/en/stable/
  - Connects to Mongo DB, hosted externally
  - Migrated from SQL as is more Pythonic
  - Contains PyPy Song list + Queue, Requests, Analytics etc


## Interfaces
### Text Chat

- **Twitch**
  - `!dmca (PyPy Song ID)` OR `!dmca (YouYube URL)` - Add a song to the queue
- **Discord**
  - `!friday` - (DJ Only) Runs setup and begins tracking for the queue
  - `!saturday` - (DJ Only) Ends all processing for the queue
  - `!lock` - (DJ Only) Locks the Queue
  - `!unlock` - (DJ Only) Unlocks the Queue

### Graphical

Bot uses 2 discord channels
- **Public Channel**
  - "PublicChannel" contains every song request that comes in from Twitch chat.
  - Click the ✕ to delete the song from queue and remove visibility
  - Click the ✓ to delete the song from queue and leave visible
- **DJ Channel**
  - "DJChannel" contains the next X songs at the front of the queue, current set to 5.
  - Click the / to refresh the embed
  - Click the 1-5 to ✓ that song request.

## Credits
*Discord/Twitch/GitLab*

###Maintainers
- **Ramiris#5376 / ramiris_ / Ramiris** *- Discord Bot setup, Server setup*
- **kittyn#0015 / kittyn / Kittyn** *- Twitch Bot setup, initial algorithms*

###Contributors
- Join us TODAY!
  
###Credits
- **Totless#0001 / totless / N/A** *- Original Concept*
- **ShiroShi#0880 / shirosh_kun / N/A** *- Profile Picture*