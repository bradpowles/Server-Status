from flask import Flask
from flask_login import LoginManager, UserMixin
from .config import Config
from .db import DB

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager()
login.init_app(app)
login.login_view = "login"
db = DB("mongodb://192.168.10.130:27017", 'sstest')

users = {'admin': {'password': 'admin'}}


class User(UserMixin):
    pass


from app import views