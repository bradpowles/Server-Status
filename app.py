from threading import Thread, Event
from updater import Updater
from app import app

thread = Thread()
thread_stop_event = Event()

if not thread.isAlive():
    print("Starting Updater")
    thread = Updater(db={"url": "mongodb://192.168.10.130:27017", "collection": "sstest"}, stop=thread_stop_event)
    thread.start()

app.run()
