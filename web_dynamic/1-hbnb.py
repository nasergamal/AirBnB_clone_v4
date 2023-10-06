#!/usr/bin/python3
''' flask/jinja '''

from flask import Flask, render_template
from markupsafe import escape
from models import storage, state, amenity, place
import uuid

app = Flask(__name__)


@app.route("/1-hbnb", strict_slashes=False)
def hbnb_html():
    '''fill up filters with db'''
    s = storage.all(state.State)
    a = storage.all(amenity.Amenity)
    p = storage.all(place.Place)
    return render_template("1-hbnb.html", states=s, amenities=a, places=p, cache_id=uuid.uuid4())


@app.teardown_appcontext
def tear_down(response_or_exc):
    '''cleanup'''
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
