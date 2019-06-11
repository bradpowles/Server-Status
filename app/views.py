from flask import render_template, redirect, flash, request, url_for
from flask_login import login_required, current_user, login_user, logout_user
from app import app, login, User, users
from .api import time, status_current


@login.user_loader
def load_user(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user


@login.request_loader
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
                           returned_statuses=status_current(),
                           time=time(),
                           autoUpdate=request.args.get("update", False, bool)
                           )
