import threading
import socket
import requests
from time import sleep
from datetime import datetime
from urllib.parse import urlparse
from pymongo import MongoClient


class DB:
    def __init__(self, url, name):
        self.__db = self.__conn(url, name)

    @staticmethod
    def __conn(url, name):
        return MongoClient(url)[name]

    def getSettings(self):
        settings = self.__db["settings"].find_one()
        return settings["refresh_interval"], settings["servers"]

    def appendStatus(self, group, name, status, time):
        status = {
            "group": group,
            "name": name,
            "status_code": status,
            "time": time.isoformat()
        }
        return self.__db["status"].insert_one(status).inserted_id


class Updater(threading.Thread):

    def __init__(self, db_host, db_collection, stop):
        self.__thread_stop_event = stop
        self.__db = DB(db_host, db_collection)
        self.__siteDown_string = "Offline"
        self.__refresh_interval, self.__servers = self.__db.getSettings()
        super(Updater, self).__init__()

    @staticmethod
    def __is_reachable(url):
        try:
            socket.gethostbyname(url)
            return True
        except socket.gaierror:
            return False
        except TypeError:
            print("Error in url: Not Valid!")
            print("Please check all URLs are valid.")
            return False

    def __get_status_code(self, url):
        try:
            status = requests.get(url, timeout=40).status_code
            return status
        except:
            return self.__siteDown_string

    def __check_single_url(self, url):
        if self.__is_reachable(urlparse(url).hostname):
            return str(self.__get_status_code(url))
        else:
            return self.__siteDown_string

    def __update_servers(self):
        for org, urls in self.__servers.items():
            for url in urls:
                self.__db.appendStatus(org, url, self.__check_single_url(url), datetime.now())

    def run(self):
        while not self.__thread_stop_event.isSet():
            self.__update_servers()
            sleep(self.__refresh_interval)
