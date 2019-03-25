from threading import Thread, Event
from updater import Updater
from app import app

thread = Thread()
thread_stop_event = Event()

if not thread.isAlive():
    thread = Updater(db_host=app.config["DB_HOST"],
                     db_collection= app.config["DB_COLLECTION"],
                     stop=thread_stop_event)
    thread.start()

app.run()
