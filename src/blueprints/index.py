"""
Index-blueprint, just a file for collecting all API-routes.
"""

import os
import re
import math
import requests
import markdown
from flask import (
    Blueprint,
    session,
    redirect,
    request,
    render_template,
    send_from_directory,
    current_app,
)

API_URL: str = os.environ.get("API_URL", "http://python-test.lenticode.com/api")
index_blueprint = Blueprint("index_blueprint", __name__, url_prefix="/")


def extract_path(url):
    match = re.search(r"http[s]?://[^/]+(/.*)", url)
    if match:
        return match.group(1)
    return "/"


@index_blueprint.context_processor
def inject_user():
    """Inject user into context."""
    user = session.get("user", None)
    if user is not None:
        user = user["user"]
    return {"user": user}


@index_blueprint.context_processor
def utility_processor():
    def max_value(a, b):
        return max(a, b)

    def min_value(a, b):
        return min(a, b)

    def total_pages(total_posts, posts_per_page):
        return math.ceil(total_posts / posts_per_page)

    def convert_md_to_html(full_text):
        return markdown.markdown(full_text)

    return dict(
        max_value=max_value,
        min_value=min_value,
        total_pages=total_pages,
        convert_md_to_html=convert_md_to_html,
    )


@index_blueprint.route("/public/users/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"] + "/users/avatars/", filename
    )


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

    return redirect(extract_path(request.referrer))


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
    page = max(int(request.args.get("page", 1)), 1)

    try:
        response = requests.get(f"{API_URL}/topics/{id_num}/page/{page}", timeout=5)
        topic_data = response.json()["data"]
    except Exception:
        pass

    return render_template(
        "topic.jinja",
        topic=topic_data.get("topic", None),
        posts=topic_data.get("posts", None),
        page=page,
    )


@index_blueprint.route("/topic/<id_num>", methods=["post"])
def create_post(id_num: int):
    """Create post route."""
    user = session.get("user", {})
    user_jwt = user.get("jwt", "")

    json_data = {"topic_id": id_num, "body": request.form.get("content")}

    try:
        requests.post(
            f"{API_URL}/posts",
            json=json_data,
            headers={"Authorization": f"Bearer {user_jwt}"},
            timeout=5,
        )
    except Exception:
        pass

    return redirect(extract_path(request.referrer))


@index_blueprint.route("/upload-image/<id_num>", methods=["post"])
def upload_image(id_num: int):
    """Upload image route."""
    user = session.get("user", {})
    user_jwt = user.get("jwt", "")
    file = request.files["file"]

    try:
        requests.post(
            f"{API_URL}/users/{id_num}/image",
            files={"file": (file.filename, file.stream, file.content_type)},
            headers={"Authorization": f"Bearer {user_jwt}"},
            timeout=5,
        )
    except Exception:
        pass

    return redirect(extract_path(request.referrer))
