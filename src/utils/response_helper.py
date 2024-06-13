"""
Class for helping creating responses
"""
from typing import Any

class ResponseHelper:
  """
  A class for creating correct responses for API.
  """
  def success_response(self, data: Any = None, message: str | None = None, status: int = 200) -> tuple[dict, int]:
    """ Creates a success response.

    Parameters:
      data (any):   Data to send in response
      message(str): Message to send in response
      status(int):  Status to use for response, default 200

    Returns:
      dict, int:    response dictionary, status
    """
    response = {
      "status": "success",
    }

    if data is not None:
      response["data"] = data

    if message is not None:
      response["message"] = message

    return response, status

  def error_response(self, errorcode: int = 400, message: str | None = None, details: str | None = None) -> tuple[dict, int]:
    """ Creates a error response.

    Parameters:
      errorcode (int):  Errorcode, default 400
      message (str):    Message to send in response
      details (str):    Details of error

    Returns:
      dict, int:        response dictionary, status
    """
    response = {
      "status": "error",
      "error": {
        "code": errorcode,
      },
    }

    if details is not None:
      response["error"]["details"] = details

    if message is not None:
      response["error"]["message"] = message

    return response, errorcode

  def unkown_error(self, details: str | None = None) -> tuple[dict, int]:
    """ Creates an unknown error

    Parameters:
      details(str): Details, if any

    Returns:
      dict, int:    response dictionary, status
    """
    response = {
      "status": "error",
      "error": {
        "code": 500,
        "message": "Unknown server error, try again."
      },
    }

    if details is not None:
      response["error"]["details"] = details

    return response, 500
