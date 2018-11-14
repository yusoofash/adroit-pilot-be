import os
from flask import Flask
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt
)
from flask_cors import CORS, cross_origin
import config
from flask_pymongo import PyMongo


mongo = None
jwt = None


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.config["MONGO_URI"] = config.MONGO_URI
    app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
    CORS(app)

    global mongo
    mongo = PyMongo(app)

    global jwt
    jwt = JWTManager(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .controller import authDto
    app.register_blueprint(authDto.bp)

    return app
