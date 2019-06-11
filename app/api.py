from app import app, db


@app.route('/api/time', methods=['GET'])
def time():
    status, updated = db.selectRecent()
    time = updated.split("T")
    time = "{0[2]}/{0[1]}/{0[0]} {1}".format(time[0].split("-"), time[1].split(".")[0])
    return time


@app.route('/api/status/current', methods=['GET'])
def status_current():
    status, updated = db.selectRecent()
    return status
