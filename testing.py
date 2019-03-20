from pymongo import MongoClient
import datetime

class DB:
    def __init__(self, url, name):
        self.__db = self.__conn(url, name)

    @staticmethod
    def __conn(url, name):
        return MongoClient(url)[name]

    def selectMostRecent(self):
        latest = self.__db["latest"].find_one()
        return self.__db["status"].find_one({"_id": latest["latest"]})


db = DB('mongodb://192.168.0.9:27017', 'sstest')
print(db.selectMostRecent())

