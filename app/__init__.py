from flask import Flask
from flask_login import LoginManager, UserMixin
from .config import Config
from .db import DB

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager()
login.init_app(app)
login.login_view = "login"
db = DB(app.config["DB_HOST"], app.config["DB_COLLECTION"])

users = {'admin': {'password': 'admin'}}


class User(UserMixin):
    pass


from app import views