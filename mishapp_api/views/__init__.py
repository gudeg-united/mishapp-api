from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask import Blueprint
from flask import jsonify
from webargs import Arg
from webargs.flaskparser import use_args

from mishapp_api.database import Disaster

disaster_api = Blueprint("disaster", __name__)


@disaster_api.errorhandler(400)
def handle_bad_request(err):
    data = getattr(err, "data")
    if data:
        err_message = data["message"]
    else:
        err_message = "Invalid request"
    return jsonify({"message": err_message}), 400


@disaster_api.route("/disasters")
@use_args({
    "page": Arg(int, default=1),
    "per_page": Arg(int, default=20),
})
def index(args):
    docs = Disaster.objects.paginate(args["page"], min(args["per_page"], 20))
    return jsonify({
        "total": docs.total,
        "page": docs.page,
        "per_page": docs.per_page,
        "items": [doc.asdict() for doc in docs.items]
    })


@disaster_api.route("/disasters/nearby")
@use_args({
    "lat": Arg(float, required=True),
    "lon": Arg(float, required=True),
    "page": Arg(int, default=1),
    "per_page": Arg(int, default=20),
})
def nearby(args):
    docs = Disaster.objects(
        geometry__coordinates__in=[args["lat"], args["lon"]]
    ).paginate(args["page"], min(args["per_page"], 20))

    return jsonify({
        "total": docs.total,
        "page": docs.page,
        "per_page": docs.per_page,
        "items": [doc.asdict() for doc in docs.items]
    })
