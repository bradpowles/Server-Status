from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId
import datetime


class DB:
    def __init__(self, url, name):
        self.__db = self.__conn(url, name)

    @staticmethod
    def __conn(url, name):
        return MongoClient(url)[name]

    def selectMostRecent(self):
        latest = self.__db["latest"].find_one()
        return self.__db["status"].find({"_id": ObjectId(latest["latest"])})

    def selectRecent(self):
        servers = self.__db["settings"].find_one()["servers"]
        recent = {}
        for group in servers:
            recent[group] = {}
            for name in servers[group]:
                for doc in self.__db["status"].find({"group": group, "name": name}).sort('time', DESCENDING):
                    recent[group][name] = doc
                    break
        return recent



db = DB('mongodb://192.168.10.130:27017', 'sstest')
print(db.selectRecent())

#client = MongoClient("mongodb://192.168.10.130:27017")
#d = client["sstest"]
#d["settings"].insert_one({"refresh_interval": 10, "offline_text": "Offline", "servers": {"brad": ["https://google.com/"], "bing": ["https://bing.com"]}})
#d["latest"].insert_one({"latest": "none"})
