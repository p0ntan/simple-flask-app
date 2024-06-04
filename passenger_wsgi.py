#!/usr/bin/env python
#
# Test project creating an API and rendering templates on same server
#
from flask import Flask
from dotenv import load_dotenv
from src.blueprints.api.apiblueprint import api_blueprint
from src.blueprints.index import index_blueprint

load_dotenv()

application = Flask(__name__)
application.register_blueprint(api_blueprint)
application.register_blueprint(index_blueprint)

if __name__ == "__main__":
  print(application.url_map)
  application.run(debug=True)
