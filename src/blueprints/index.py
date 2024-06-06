"""
Index-blueprint, just a file for collecting all API-routes.
"""
import os
import requests
from flask import Blueprint, render_template

index_blueprint = Blueprint('index_blueprint', __name__, url_prefix="/")

@index_blueprint.route("/")
def index():
  return render_template("index.html")