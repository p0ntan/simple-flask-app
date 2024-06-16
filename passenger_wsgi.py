#!/usr/bin/env python
#
# Test project creating an REST-API for an online forum. Views is also
# rendered for a simple page using the API.
#
from config import get_config
from flask import Flask
from src.blueprints.api.apiblueprint import api_blueprint
from src.blueprints.index import index_blueprint

from flask_jwt_extended import JWTManager

def create_app():
    application = Flask(__name__)
    application.config.from_object(get_config())

    jwt = JWTManager()
    jwt.init_app(application)

    application.register_blueprint(api_blueprint)
    application.register_blueprint(index_blueprint)

    return application

# application needs to be here for passenger to access it on server
application = create_app()

if __name__ == "__main__":
    application.run()
