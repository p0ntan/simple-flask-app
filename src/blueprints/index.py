"""
Index-blueprint, just a file for collecting all API-routes.
"""

import os
import requests
from flask import Blueprint, session, redirect, request, render_template

API_URL: str = os.environ.get("API_URL", "http://python-test.lenticode.com/api")
index_blueprint = Blueprint("index_blueprint", __name__, url_prefix="/")


@index_blueprint.context_processor
def inject_user():
    """Inject user into context."""
    user = session.get("user", None)
    return {"user": user}


@index_blueprint.route("/")
def index():
    """Index route for page."""

    return render_template("index.jinja")


@index_blueprint.route("/login", methods=["post"])
def login():
    """Login route."""
    username = request.form["username"]

    try:
        response = requests.post(
            API_URL + "/users/login", json={"username": username}, timeout=5
        )
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


@index_blueprint.route("/new-topics", methods=["get"])
def new_topics():
    """Latest topics route."""
    try:
        response = requests.get(API_URL + "/topics/latest", timeout=5)
        topics = response.json()["data"]
    except Exception:
        topics = []

    return render_template("new-topics.jinja", topics=topics)


@index_blueprint.route("/topic/<id_num>", methods=["get"])
def single_topic(id_num: int):
    """Latest topics route."""
    topic_data = {}
    page = request.args.get("page", 0)

    try:
        response = requests.get(f"{API_URL}/topics/{id_num}/page/{page}", timeout=5)
        topic_data = response.json()["data"]
    except Exception:
        pass

    return render_template(
        "topic.jinja",
        topic=topic_data.get("topic", None),
        posts=topic_data.get("posts", None),
    )
