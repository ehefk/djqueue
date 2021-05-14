# djqueue
DJ Queue bot for Just Dance Streams using Discord and Twitch

- ***PythonTwitchBotFramework*** - Twitch IRC w PubSub client  https://pypi.org/project/PythonTwitchBotFramework/
  - Might be able to get away from this in a future iteration
  - Need to setup pubsub if want to handle point requests instead of chat messages; would be more efficient

- ***discord.py*** - Discord queue, stats, control panel https://discordpy.readthedocs.io/en/stable/ 


### Chat Interface:

`!dmca #justdance`

`!dmca youtubeurl`

### Discord Interface:

Bot uses 2 discord channels
- Channel 1 contains every song request that comes in
- Channel 2 contains the next X songs at the front of the queue, current set to 3
  - Would like to make 1 be for marshal queue and 1 for request spam randomizer queue

- Click the ✕ to delete the song from queue and remove visibility
- Click the ✓ to delete the song from queue and leave visible (or mark song green ONLY if in channel 1)
