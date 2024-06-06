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

load_dotenv()

application = Flask(__name__)
application.register_blueprint(api_blueprint)
application.register_blueprint(index_blueprint)
application.secret_key = os.environ.get("SECRET_KEY", re.sub(r"[^a-z\d]", "", os.path.realpath(__file__)))

if __name__ == "__main__":
  print(application.url_map)
  application.run(debug=True)
