from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask import Blueprint
from flask import jsonify
from webargs import Arg
from webargs import ValidationError
from webargs.flaskparser import use_args

from mishapp_api.database import Disaster

disaster_api = Blueprint("disaster", __name__)


def radius_gte_zero(val):
    if val < 0:
        raise ValidationError("radius must greater than equal 0")


@disaster_api.errorhandler(400)
def handle_bad_request(err):
    data = getattr(err, "data")
    if data:
        err_message = data["message"]
    else:
        err_message = "Bad request"
    return jsonify({"message": err_message}), 400


@disaster_api.errorhandler(404)
def handle_not_found(err):
    return jsonify({"message": "Not found"}), 404


@disaster_api.route("/disasters")
@use_args({
    "page": Arg(int, default=1),
    "per_page": Arg(int, default=20),
    "category": Arg(str),
})
def index(args):
    q = Disaster.objects
    if args["category"]:
        q = q(properties__type=args["category"])
    docs = q.paginate(args["page"], min(args["per_page"], 20))

    return jsonify({
        "meta": {
            "total": docs.total,
            "page": docs.page,
            "per_page": docs.per_page,
        },
        "items": [doc.asdict() for doc in docs.items]
    })


@disaster_api.route("/disasters/nearby")
@use_args({
    "lat": Arg(float, required=True),
    "lon": Arg(float, required=True),
    "radius": Arg(float, validate=radius_gte_zero, required=True),
    "page": Arg(int, default=1),
    "per_page": Arg(int, default=20),
    "category": Arg(str),
})
def nearby(args):
    q = Disaster.objects(
        geometry__near={
            "$geometry": {
                "type": "Point",
                "coordinates": [args["lon"], args["lat"]],
            },
            "$maxDistance": args["radius"],
        },
    )
    if args["category"]:
        q = q(properties__type=args["category"])
    docs = q.paginate(args["page"], min(args["per_page"], 20))

    return jsonify({
        "meta": {
            "total": docs.total,
            "page": docs.page,
            "per_page": docs.per_page,
        },
        "items": [doc.asdict() for doc in docs.items]
    })


@disaster_api.route("/disasters/verify")
@use_args({
    "lat": Arg(float, required=True),
    "lon": Arg(float, required=True),
    "radius": Arg(float, validate=radius_gte_zero, required=True),
    "category": Arg(str),
})
def verify(args):
    q = Disaster.objects(
        geometry__near={
            "$geometry": {
                "type": "Point",
                "coordinates": [args["lon"], args["lat"]],
            },
            "$maxDistance": args["radius"],
        },
    )
    if args["category"]:
        q = q(properties__type=args["category"])
    counter = q.count()

    if counter > 0:
        return jsonify({"message": "OK"})
    return jsonify({"message": "Not found"}), 404


@disaster_api.route("/disasters/<id>")
def get(id):
    disaster = Disaster.objects.get_or_404(id=id)
    return jsonify(disaster.asdict())
