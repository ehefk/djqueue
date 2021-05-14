import pymongo
import json
import datetime


class Main:
    def __init__(self):
        with open("secrets.json", "r") as file:
            secrets = json.load(file)
        self.client = pymongo.MongoClient(secrets["MongoDBToken"])
        self.db = self.client['DJ_Fry']

    def create_request(self, User, URI, TimesPlayed, Status="Pending", Tags=[]):
        request = {"User": User,
                   "URI": URI,
                   "Timestamp": datetime.datetime.utcnow(),
                   "Status": Status,
                   "DiscordMessageID": 0,
                   "TimesRequested": 1,
                   "TimesPlayed": TimesPlayed}
        self.db["Requests"].insert_one(request)
