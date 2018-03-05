#!/usr/bin/python
# todo:reorder and rearrange
from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine
import os
import sys

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../../')))


db = MongoEngine()


def create_app(**config_overrides):
    app = Flask(__name__, static_folder='static', static_url_path='')

    # Load config.
    from views import views
    app.register_blueprint(views)

    # apply overrides
    app.config.update(config_overrides)

    # Setup the database.
    db.init_app(app)

    return app


# app = create_app(
    # MONGODB_SETTINGS={'db': 'db_deploy', 'host': 'mongodb'},
    # TESTING=True,
    # SALT='IfHYBwi5ZUFZD9VaonnK',
# )
# app = None
# SALT = 'dfdf'
# SALT = app.config.get('SALT')


# Enable cross origin sharing for all endpoints

if __name__ == '__main__':
    # Change the working directory to the script directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    app = create_app(
        MONGODB_SETTINGS={'db': 'db_deploy', 'host': 'mongodb'},
        TESTING=True,
        SALT='IfHYBwi5ZUFZD9VaonnK',
    )
    CORS(app)

    # Run the application
    app.run(debug=False, port=8080, host="0.0.0.0")
