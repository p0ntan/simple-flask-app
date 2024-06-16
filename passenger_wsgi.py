#!/usr/bin/env python
#
# Test project creating an API and rendering templates on same server
#
from config import get_config
from flask import Flask
from src.blueprints.api.apiblueprint import api_blueprint
from src.blueprints.index import index_blueprint

from flask_jwt_extended import JWTManager

# application = Flask(__name__)
# application.secret_key = os.environ.get("SECRET_KEY", re.sub(r"[^a-z\d]", "", os.path.realpath(__file__)))
# application.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET", "this-is-just-a-not-secret-backup-key")
# jwt = JWTManager(application)

# application.register_blueprint(api_blueprint)
# application.register_blueprint(index_blueprint)

def create_app():
    application = Flask(__name__)
    application.config.from_object(get_config())

    jwt = JWTManager()
    jwt.init_app(application)

    application.register_blueprint(api_blueprint)
    application.register_blueprint(index_blueprint)

    return application

if __name__ == "__main__":
    application = create_app()
    application.run()
