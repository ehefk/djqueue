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


Song Data

```json
{
  "songId": 0,
  "songInfo": {
    "songArtist": "GHOSTDATA_",
    "songName": "Full Bodied",
    "songURI": "uri"
  },
  
  "songStats": {
    "songLength": 120,   #in seconds
    "timesPlayed": 999,
    "timesRequested": 1234,
  }
}
```

Queue Data Node - Actually a doubly linked list

```json
{
  "next": "next",
  "prev": "prev",
  "queuePos": 7,
  "data": {
    "songId": 0,
    "songTitle": "GHOSTDATA_ Full Bodied",
    "songURI": "uri",
    "songLength": 120,   #in seconds
    "queueETA": 120   #in seconds
    "timesPlayedToday": 3,
    "timesRequestedToday": 6
  }
