from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask.ext.script import Manager

from mishapp_api import create_app
from mishapp_api.helpers.usgs import fetch_hourly_data
from mishapp_api.database import Disaster


def main():
    manager = Manager(create_app)

    @manager.command
    def usgs():
        """Fetches data from USGS
        """
        data = fetch_hourly_data()
        for item in data["features"]:
            # TODO: use upsert!
            if not Disaster.objects(source="usgs", source_id=item["id"]).count():  # noqa
                disaster = Disaster()
                disaster.source = "usgs"
                disaster.source_id = item["id"]
                disaster.type = item["properties"]["type"]
                disaster.properties = item["properties"]
                disaster.geometry = item["geometry"]
                disaster.save()
    manager.run()


if __name__ == "__main__":
    main()