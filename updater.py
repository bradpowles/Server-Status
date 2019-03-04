import threading
import socket
import requests
from time import sleep
from urllib.parse import urlparse


class Results:

    def __init__(self):
        self.__returned_statuses = {}

    def get(self):
        return self.__returned_statuses

    def set(self, statuses):
        self.__returned_statuses = statuses


class Updater(threading.Thread):

    def __init__(self, settings, results_store, stop):
        self.__settings_handler(settings)
        self.__results = results_store
        self.__thread_stop_event = stop

        super(Updater, self).__init__()

    def __settings_handler(self, settings):
        try:
            self.__to_check = settings["servers"]
            self.__siteDown_string = settings["offline_text"]
            self.__refresh_interval = settings["refresh_interval"]
        except KeyError:
            self.__to_check = {"Default": ["https://broken.config.file"]}
            self.__siteDown_string = "503"
            self.__refresh_interval = 60

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
        statuses = {}
        for org, urls in self.__to_check.items():
            statuses[org] = {}
            for url in urls:
                statuses[org][url] = self.__check_single_url(url)
        self.__results.set(statuses=statuses)

    def run(self):
        while not self.__thread_stop_event.isSet():
            self.__update_servers()
            sleep(self.__refresh_interval)
