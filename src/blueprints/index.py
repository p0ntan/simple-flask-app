"""
Index-blueprint, just a file for collecting all API-routes.
"""
import os
import requests
from flask import Blueprint, render_template

index_blueprint = Blueprint('index_bluepring', __name__, url_prefix="/")

@index_blueprint.route("/")
def index():
  url = os.environ.get("API_URL", "")
  print(url)
  r = requests.get(f"{url}/topic/2")
  data = r.json()
  return render_template("index.html", posts=data["data"]["posts"])