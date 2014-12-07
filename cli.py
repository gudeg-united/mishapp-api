from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask.ext.script import Manager

from mishapp_api import create_app
from mishapp_api.helpers import usgs as _usgs
from mishapp_api.helpers import gdacs as _gdacs
from mishapp_api.database import Disaster


def main():
    manager = Manager(create_app)

    @manager.command
    def usgs():
        """Fetches data from USGS
        """
        data = _usgs.fetch_hourly_data()
        for item in data["features"]:
            item["source"] = "usgs"
            item["geometry"]["coordinates"].pop()
            Disaster.create_unique(**item)

    @manager.command
    def gdacs():
        """Fetches data from gdacs
        """
        data = _gdacs.fetch_daily_data()
        for item in data:
            item["source"] = "gdacs"
            Disaster.create_unique(**item)

    manager.run()


if __name__ == "__main__":
    main()
