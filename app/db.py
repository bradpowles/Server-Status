from pymongo import MongoClient, DESCENDING


class DB:
    def __init__(self, url, name):
        self.__db = self.__conn(url, name)

    @staticmethod
    def __conn(url, name):
        return MongoClient(url)[name]

    def selectMostRecent(self):
        latest = self.__db["latest"].find_one()
        return self.__db["status"].find_one({"_id": latest["latest"]})

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
