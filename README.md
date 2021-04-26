# djqueue
DJ Queue bot for Just Dance Streams using Discord and Twitch

#### PythonTwitchBotFramework - Twitch IRC w PubSub client
#### discord.py - Discord queue, stats, control panel

- User requests with points - uses Twitch PubSub client to track
- Bot rejects requests that aren't a URL or song number in the database
- Points refunded after request processed

- Tracks number of times song requested during current session & all time

  > "@xxx Song # or YT link plz"
  > "Artist - Title placed #xx in queue.  ETA: xx:xx  Requested X times today."

- DJ Controls Queue using reactions to bot's recent 5 posts in #DJQueue channel

