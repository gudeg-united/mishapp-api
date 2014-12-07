from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime
from flask.ext.mongoengine import MongoEngine

db = MongoEngine()


class Disaster(db.Document):
    source = db.StringField(required=True)
    source_id = db.StringField(required=True)
    type = db.StringField()
    properties = db.DictField()
    geometry = db.DictField()
    modified_at = db.DateTimeField(default=datetime.utcnow)

    meta = {
        "indexes": [[("geometry", "2dsphere")]],
    }

    def asdict(self):
        return {
            "id": "{}".format(self["id"]),
            "source": self["source"],
            "source_id": self["source_id"],
            "type": self["type"],
            "properties": self["properties"],
            "geometry": self["geometry"],
        }

    @classmethod
    def create_unique(cls, **fields):
        # TODO: use upsert!
        if not cls.objects(source=fields["source"], source_id=fields["id"]).count():  # noqa
            disaster = Disaster()
            disaster.source = fields["source"]
            disaster.source_id = fields["id"]
            disaster.type = "Feature"
            disaster.properties = fields["properties"]
            disaster.geometry = fields["geometry"]
            disaster.save()
            return disaster
