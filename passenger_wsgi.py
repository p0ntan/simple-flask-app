#!/usr/bin/env python
#
# Test project creating an API and rendering templates on same server
#
import re
import os
from flask import Flask
from dotenv import load_dotenv
from src.blueprints.api.apiblueprint import api_blueprint
from src.blueprints.index import index_blueprint

from flask_jwt_extended import JWTManager

load_dotenv()

application = Flask(__name__)
application.secret_key = os.environ.get("SECRET_KEY", re.sub(r"[^a-z\d]", "", os.path.realpath(__file__)))
application.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET", "this-is-just-a-not-secret-backup-key")
jwt = JWTManager(application)

application.register_blueprint(api_blueprint)
application.register_blueprint(index_blueprint)

if __name__ == "__main__":
  print(application.url_map)
  application.run(debug=True)
