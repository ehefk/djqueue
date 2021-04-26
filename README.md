# djqueue
DJ Queue bot for Just Dance Streams using Discord and Twitch

- ***PythonTwitchBotFramework*** - Twitch IRC w PubSub client  https://pypi.org/project/PythonTwitchBotFramework/
- ***discord.py*** - Discord queue, stats, control panel https://discordpy.readthedocs.io/en/stable/ 

- User requests with points - uses Twitch PubSub client to track
  - Bot rejects requests that aren't a URL or song number in the database
  - Points refunded after request processed

- Queue controlled in Discord channel, by reaction to recent bot posts
  - Display unknown url metadata for DJ approval

- Track duplicate requests per session & all time
  - Alert DJ to duplicates in queue or reject if played too recently


Twitch Output Example:

  > "@xxx Song # or YT link plz"
  
  > "Artist - Title placed #xx in queue.  ETA: xx:xx  Requested X times today."


