from flask import Flask, Response, request
import requests
from flask_table import Table, Col
from datetime import datetime
import pytz
import seatLayout

from flask import Flask
from flask_cors import CORS, cross_origin
from flask_caching import Cache

utc = pytz.utc
est = pytz.timezone('US/Eastern')


def convert_to_est(time_str):
    utc_time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
    utc_time = utc.localize(utc_time)  # Localize to UTC
    est_time = utc_time.astimezone(est)  # Convert to EST
    return est_time.strftime("%H:%M %B %d, %Y")


app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CORS_HEADERS": "Content-Type"
}

app.config.from_mapping(config)
cache = Cache(app)


@app.route("/<train>")
@cache.cached(timeout=10)
def frontend(train):
    try:
        data = get_data()[train]
    except KeyError:
        return Response("{text: no}", 400)

    # Declare your table
    class ItemTable(Table):
        station = Col('Station')
        estimated = Col('Estimated')
        scheduled = Col('Scheduled')

    class Item(object):
        def __init__(self, station, estimated, scheduled):
            self.station = station
            self.estimated = estimated
            self.scheduled = scheduled

    items = [Item(x["station"], convert_to_est(x["estimated"]), convert_to_est(x["scheduled"])) for x in
             data['times']]

    table = ItemTable(items)

    return table.__html__()

@app.route("/trains")
def car_types():
    train_number = request.args.get("number")
    date = request.args.get("date")
    # print(train_number, date)

    return seatLayout.get_car_data(train_number, date)

def get_data():
    # print("Getting Times")
    data = requests.get("https://tsimobile.viarail.ca/data/allData.json")

    return data.json()


if __name__ == '__main__':
    app.run(port=8000)
