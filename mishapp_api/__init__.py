from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask import Flask
from flask.ext.appconfig import AppConfig

from mishapp_api.database import db
from mishapp_api.views import disaster_api


def create_app():
    app = Flask(__name__)
    AppConfig(app, default_settings="mishapp_api.default_config")
    db.init_app(app)
    app.register_blueprint(disaster_api)
    return app
