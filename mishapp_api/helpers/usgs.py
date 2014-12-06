from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# import arrow
import requests

_BASE_URL = "http://earthquake.usgs.gov/earthquakes/feed/v1.0"
_req = requests.Session()


def fetch_hourly_data():
    resp = _req.get(_BASE_URL + "/summary/all_hour.geojson")
    if resp.status_code != 200:
        return
    return resp.json()


def fetch_detail(url):
    resp = _req.get(url)
    if resp.status_code != 200:
        return
    return resp.json()
