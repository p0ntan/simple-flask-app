"""
Simple class to use when checking for permissions
"""


class Permission:
    """Simple class to use when checking for permissions for a user"""

    def __init__(self, permission_data: dict):
        """
        Args:
          permission_data(dict): dictionary with permissions
        """
        self._post = {
            "edit": permission_data.get("edit_post", False),
            "delete": permission_data.get("delete_post", False)
        }
        self._topic = {
          "edit": permission_data.get("edit_topic", False),
          "delete": permission_data.get("delete_topic", False)
        }
        self._user = {
          "edit": permission_data.get("edit_user", False),
          "delete": permission_data.get("delete_user", False)
        }

    def edit_post(self):
        return self._post["edit"]
  
    def delete_post(self):
        return self._post["delete"]

    def edit_topic(self):
        return self._topic["edit"]
  
    def delete_topic(self):
        return self._topic["delete"]

    def edit_user(self):
        return self._user["edit"]

    def delete_user(self):
        return self._user["delete"]
