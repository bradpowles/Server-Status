from app.config import Config
from pymongo import MongoClient

# Servers
servers = {
    "refresh_interval": 10,
    "servers": {
        "grouping": ["https://bar.com", "https://foo.bar.com"]
    }
}

# Setup Database Settings
db = MongoClient(Config.DB_HOST)[Config.DB_COLLECTION]
print("Connected to MongoDB.")
db["settings"].drop()
print("Removed Previous Settings")
db["settings"].insert_one(servers)
print("Added new settings to MongoDB... Setup Complete.")
