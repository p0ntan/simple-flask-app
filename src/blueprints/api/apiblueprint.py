"""
API-blueprint, just a file for collecting all API-routes.
"""
from flask import Blueprint
from src.blueprints.api.userblueprint import user_blueprint

api_blueprint = Blueprint('api_blueprint', __name__, url_prefix="/api")
api_blueprint.register_blueprint(user_blueprint)
