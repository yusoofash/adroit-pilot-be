import os
from flask import Flask
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt
)
from flask_cors import CORS, cross_origin
import config
from flask_pymongo import PyMongo
import cloudinary

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

    cloudinary.config(
        cloud_name=config.CLOUDINARY_CLOUD_NAME,
        api_key=config.CLOUDINARY_API_KEY,
        api_secret=config.CLOUDINARY_API_SECRET
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .controller import authDto, companyDto
    app.register_blueprint(authDto.bp)
    app.register_blueprint(companyDto.company_api)

    return app
