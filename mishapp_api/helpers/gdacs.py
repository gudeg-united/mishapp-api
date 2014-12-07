from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from datetime import datetime
from datetime import timedelta

import requests
from pyquery import PyQuery as pq

_BASE_URL = (
    "http://www.gdacs.org/transform.aspx?"
    "xmlurl=http://www.gdacs.org/rss.aspx%3Fprofile%3DARCHIVE"
    "%26from%3D2014-12-07%26to%3D2014-12-07%26alertlevel%3D"
    "%26country%3D%26eventtype%3DEQ,TC,FL&"
    "xslurl=http://www.gdacs.org/xslt/gdacs_table.xslt"
    "&pname=|eventtypes&pvalue=|EQ,TC,FL"
    )

DISASTER_TYPE_MAPPER = {
    "Earthquakes": "earthquake",
    "Tropical cyclones": "tornado",
    "Floods": "flood",
}

_RE_WHITESPACE = re.compile("\s+")

_req = requests.Session()


def get_url(from_date, to_date):
    base = (
        "http://www.gdacs.org/transform.aspx?"
        "xmlurl=http://www.gdacs.org/rss.aspx%3Fprofile%3DARCHIVE"
        "%26from%3D{from_date}%26to%3D{to_date}%26alertlevel%3D"
        "%26country%3D%26eventtype%3DEQ,TC,FL&"
        "xslurl=http://www.gdacs.org/xslt/gdacs_table.xslt"
        "&pname=|eventtypes&pvalue=|EQ,TC,FL"
    )
    url = base.format(from_date=from_date, to_date=to_date)
    return url


def extract_report(type_, el):
    row = dict(zip(
        ["id", "country", "mag", "date", "impact", "coord"],
        filter(None, [pq(e).text() for e in el.find("td")]),
    ))
    row["properties"] = {
        "country": row.pop("country"),
        "mag": row.pop("mag"),
        "date": row.pop("date"),
        "impact": row.pop("impact"),
        "type": type_,
    }
    lat, lon = _RE_WHITESPACE.sub("", row.pop("coord")).split(",")
    row["geometry"] = {
        "type": "Point",
        "coordinates": [float(lon), float(lat)],
    }
    row["type"] = "Feature"
    return row


def fetch_daily_data():
    today = datetime.utcnow()
    yesterday = today - timedelta(days=1)
    url = get_url(yesterday.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"))

    resp = _req.get(url)
    if resp.status_code != 200:
        return

    dom = pq(resp.text)
    last_known_category = ""
    data = []

    for el in dom.find("tr").items():
        item = {}
        category = DISASTER_TYPE_MAPPER.get(el.find("h4 a").text())

        if category:
            last_known_category = category
            continue

        if len(el.find("th")) > 0:
            continue

        item["category"] = last_known_category
        item.update(extract_report(item["category"], el))
        data.append(item)
    return data
