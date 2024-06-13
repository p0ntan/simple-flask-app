"""
Different types for data.
"""
from typing import TypedDict


class UserInput(TypedDict):
  """UserInput."""
  username: str
  role: str
  signature: str | None
  avatar: str | None


class UserData(UserInput):
  """UserData representing user data."""
  user_id: int


class TopicType(TypedDict):
  """Topic type."""
  topic_id: int
  title: str
  category: int
  created: str
  last_edited: str | None
  deleted: str | None
  disabled: bool

class TopicData(TopicType, total=False):
  """Topic data."""
  created_by: UserData


class PostType(TypedDict):
  """PostType, base for PostData."""
  post_id: int
  topic_id: int
  created: str
  last_edited: str | None
  deleted: str | None
  title: str | None
  body: str


class PostData(PostType, total=False):
  """PostData"""
  author: UserData