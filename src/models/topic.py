"""
Topic model representing a topic.
"""

from __future__ import annotations
from typing import Any
from src.models.user import User
from src.errors.customerrors import UnauthorizedException, NoDataException
from src.utils.daos import TopicDAO
from src.static.types import TopicData


class Topic:
    """Topic model representing a topic."""

    def __init__(self, author: User, topic_data: TopicData):
        """Initiate a topic.

        Parameters:
          author (User):          User who created the topic
          topic_data (TopicData): Dictonary with needed data for topic with keys
            - topic_id (int):               id for topic
            - title (str):                  title for topic
            - category (int):               id for category
            - created (str):                timestamp when topic was created
            - last_edited (str | None):     timestamp when topic was last edited
            - deleted (str | None):         timestamp when topic was deleted (softly)
            - disabled (bool):              boolean if topic is disabled

        Raises:
          KeyError: In case of missing required keys
        """
        self._topic_id = topic_data["topic_id"]
        self._created_by = author
        self._title = topic_data["title"]
        self._category = topic_data["category"]
        self._created = topic_data["created"]
        self._last_edited = topic_data.get("last_edited", None)
        self._deleted = topic_data.get("deleted", None)
        self._disabled = topic_data.get("disabled", False)

    def update(self, topic_data: dict[str, Any], editor: User) -> dict[str, Any]:
        """Update the topic, only updating avalible attributes for editor based on editor's access to post.

        Args:
          topic_data (dict):      Dictionary with keys to update.
          editor (User):          The user who is wanting to update the topic.

        Returns:
          new_data (dict):        Dict with only the updated data.

        Raises:
          UnauthorizedException: If the user is not authorized to manage the topic.
        """
        if not self.editor_has_permission(editor, "update"):
            raise UnauthorizedException("User not authorized to update topic.")

        # Update logic below.
        self._title = topic_data.get("title", self._title)

        return {"title": self._title}

    def editor_has_permission(self, editor: User, action: str) -> bool:
        """Control that another user (editor) can manage the topic based on id and access.

        Args:
          editor (User):          The editor to control having access to manage this topic.
          action (str):           String with wanted action like update or delete.

        Returns:
          has_permission (bool):  True if edditor has permission, False if not.
        """
        # TODO add more (better) logic when time comes, like admin/moderator.
        if action == "update":
            return editor.id == self._created_by.id or editor.permission.edit_topic()
        elif action == "delete":
            return editor.id == self._created_by.id or editor.permission.delete_topic()
        return False  # Default value

    def to_dict(self) -> TopicData:
        """Return topic data as dictionary.

        Returns:
          (dict): Dictionary with topic data
        """
        result = {}

        for key, value in self.__dict__.items():
            key = key[1:] if key[0] == "_" else key
            result[key] = value.to_dict() if hasattr(value, "to_dict") else value

        return TopicData(**result)

    @classmethod
    def from_db_by_id(cls, topic_id: int, topic_dao: TopicDAO) -> Topic:
        """Initiate topic with data from database, by id.

        Parameters:
          topic_id (int):       The id of the topic.
          topic_dao (TopicDAO): An instance of the TopicDAO class.

        Returns:
          Topic:                The topic object.

        Raises:
          NoDataException:      If no topic is found with given id.
        """
        topic_data = topic_dao.get_one(topic_id)

        if topic_data is None:
            raise NoDataException(f"No topic found with id: {topic_id}")

        user_data = topic_data.pop("created_by")

        return cls(User(user_data), topic_data)
