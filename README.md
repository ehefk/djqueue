# djqueue
DJ Queue bot for Just Dance Streams using Discord and Twitch

- ***PythonTwitchBotFramework*** - Twitch IRC w PubSub client  https://pypi.org/project/PythonTwitchBotFramework/
  - Might be able to get away from this in a future iteration
  - Need to setup pubsub if want to handle point requests instead of chat messages; would be more efficient

- ***discord.py*** - Discord queue, stats, control panel https://discordpy.readthedocs.io/en/stable/ 


### Chat Interface:

!dmca #justdance
!dmca youtubeurl

### Discord Interface:

Bot uses 2 discord channels
- Channel 1 contains every song request that comes in
- Channel 2 contains the next X songs at the front of the queue

- Click the X to delete the song from queue and remove visibility
- Click the :Check: to delete the song from queue and leave visible (or mark song green ONLY if in channel 1)
