# djqueue
DJ Queue bot for Just Dance Streams using Discord and Twitch

1. **PythonTwitchBotFramework** - Twitch IRC w PubSub client
2. **discord.py** - Discord queue, stats, control panel

- User requests with points - uses Twitch PubSub client to track
  - Bot rejects requests that aren't a URL or song number in the database
  - Points refunded after request processed

- Queue controlled in Discord channel, by reaction to recent bot posts
- Number of requests tracked per session & all time

Twitch Output Example:

  > "@xxx Song # or YT link plz"
  
  > "Artist - Title placed #xx in queue.  ETA: xx:xx  Requested X times today."

