"""
Different types for data.
"""

from typing import TypedDict


class UserType(TypedDict):
    """UserInput."""

    user_id: int
    username: str
    role: str


class UserData(UserType, total=False):
    """UserData representing user data."""

    signature: str | None
    avatar: str | None


class TopicType(TypedDict):
    """Topic type, base for required keys."""

    topic_id: int
    title: str
    category: int
    created: str
    disabled: bool


class TopicData(TopicType, total=False):
    """Topic data, with optional keys."""

    created_by: UserData
    last_edited: str | None
    deleted: str | None


class PostType(TypedDict):
    """PostType, base for PostData with required keys."""

    post_id: int
    topic_id: int
    created: str
    body: str


class PostData(PostType, total=False):
    """PostData, with optional keys"""

    author: UserData
    last_edited: str | None
    deleted: str | None
    title: str | None
