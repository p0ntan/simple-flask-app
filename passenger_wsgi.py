#!/usr/bin/env python
# Important to use application and not app for start with passenger

from flask import Flask
from src.blueprints.api.apiblueprint import api_blueprint

application = Flask(__name__)

application.register_blueprint(api_blueprint)

if __name__ == "__main__":
  print(application.url_map)
  application.run()
