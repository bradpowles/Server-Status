# Server Status Website

A program using Python Flask to display the status code's of provided websites.

##Prerequisites

- Python 3.6+
- requirements.txt
- MongoDB - Running without authentication

##Installation Instructions

Edit the app/config.py to reflect the url to your MongoDB
```python
class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = 'guess-me-if-you-can'
    DB_HOST = 'mongodb://127.0.0.1:27017' # Database Server URL
    DB_COLLECTION = 'server-status' # Database Name
```

Then edit the `setup.py` file to reflect the servers you wish to monitor.

```python
# Servers
servers = {
    "refresh_interval": 10, # Time between servers should be pinged.
    "servers": {
        "grouping": [ # Name of the group of websites in the list.
            "https://bar.com", 
            "https://foo.bar.com"
        ]
    }
}
```

Following this, run `setup.py` to initialise the database.

*Edit and run the setup.py each time you wish to change server addresses or refresh interval.*

## Running Server Status

`python run.py`