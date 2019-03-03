import json
from flask import Flask, render_template, jsonify
from updater import *
from threading import Thread, Event
import os

try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')) as f:
        to_check = json.load(f)
except FileNotFoundError:
    print("ERROR: Please ensure that there is a config.json file in the same directory. Example: example-config.json")
    quit()

app = Flask(__name__)

thread = Thread()
thread_stop_event = Event()

global results
results = Results()


@app.route("/", methods=["GET"])
def display_returned_statuses():
    return render_template('returned_statuses.html', returned_statuses=results.get())


if __name__ == '__main__':
    if not thread.isAlive():
        print("Starting Updater")
        thread = Updater(settings=to_check, results_store=results, stop=thread_stop_event)
        thread.start()
    app.run()
