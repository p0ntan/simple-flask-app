"""
Index-blueprint, just a file for collecting all API-routes.
"""
import os
import requests
from flask import Blueprint, session, redirect, request, render_template

API_URL: str = os.environ.get("API_URL", "")
index_blueprint = Blueprint('index_blueprint', __name__, url_prefix="/")


@index_blueprint.route("/")
def index():
  """Index route for page."""
  user = session.get("user", None)

  return render_template("index.jinja", user=user)


@index_blueprint.route("/login", methods=["post"])
def login():
  """Login route."""
  username = request.form['username']
  
  try:
    response = requests.post(API_URL + "/users/login", json={"username": username}, timeout=5)
    user = response.json()
    session["user"] = user["data"]
  except Exception:
    # Do nothing, just catch error
    pass

  return redirect("/")


@index_blueprint.route("/logout", methods=["post"])
def logout():
  """Logout route."""
  session.pop("user")

  return redirect("/")
