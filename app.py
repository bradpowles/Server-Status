import json
from flask import Flask, render_template, abort, redirect, flash, request, url_for
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
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
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

users = {'admin': {'password': 'admin'}}


class User(UserMixin):
    pass


@login_manager.user_loader
def load_user(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(r):
    username = r.form.get('username')
    if username not in users:
        return
    user = User()
    user.id = username
    if r.form['password'] == users[username]['password']:
        return user
    else:
        return


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    if request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        login_user(user)
        return redirect(url_for('dashboard'))
    flash("Error: Logging In")
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/")
def index():
    return render_template("index.html", user=current_user)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('returned_statuses.html',
                           user=current_user,
                           returned_statuses=results.get(),
                           time=results.get_time(),
                           autoUpdate=request.args.get("update", False, bool)
                           )


thread = Thread()
thread_stop_event = Event()

global results
results = Results()

if __name__ == '__main__':
    if not thread.isAlive():
        print("Starting Updater")
        thread = Updater(settings=to_check, results_store=results, stop=thread_stop_event)
        thread.start()
    app.run()
