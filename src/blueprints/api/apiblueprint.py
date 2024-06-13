"""
API-blueprint, just a file for collecting all API-routes.

This is also the place for handling errors.
"""
from flask import Blueprint
from src.blueprints.api.userblueprint import user_blueprint
from src.blueprints.api.postblueprint import post_blueprint
from src.blueprints.api.topicblueprint import topic_blueprint
from src.utils.response_helper import ResponseHelper
from src.errors.customerrors import NoDataException, InputInvalidException, UnauthorizedException

r_helper = ResponseHelper()

api_blueprint = Blueprint('api_blueprint', __name__, url_prefix="/api")
api_blueprint.register_blueprint(user_blueprint)
api_blueprint.register_blueprint(post_blueprint)
api_blueprint.register_blueprint(topic_blueprint)

# Error handling
@api_blueprint.errorhandler(Exception)
def _handle_api_error(error):
  if isinstance(error, (NoDataException, InputInvalidException, UnauthorizedException)):
    response, status = r_helper.error_response(error.status, details=f"{error}")
  else:
    response, status = r_helper.unkown_error(details=f"{error}")
  return response, status
