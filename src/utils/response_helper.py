"""
Class for helping creating responses
"""


class ResponseHelper:
  """
  A class for creating correct responses for API.
  """
  def success_response(self, data: any = None, message: str = None) -> dict:
    """ Creates a success response.

    Parameters:
      data (any):   Data to send in response
      message(str): Message to send in response

    Returns:
      dict:         Dictonary to send as a response
    """
    response = {
      "status": "success",
    }

    if data is not None:
      response["data"] = data

    if message is not None:
      response["message"] = message

    return response

  def error_response(self, errorcode: int = 400, message: str = None, details: str = None) -> dict:
    """ Creates a error response.

    Parameters:
      errorcode (int):  Errorcode, default 400
      message (str):    Message to send in response
      details (str):    Details of error

    Returns:
      dict:             Dictonary to send as a response
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

    return response

  def unkown_error(self, details: str = None) -> dict:
    """ Creates an unknown error"""
    response = {
      "status": "error",
      "error": {
        "code": 500,
        "message": "Unknown server error, try again."
      },
    }

    if details is not None:
      response["error"]["details"] = details

    return response
