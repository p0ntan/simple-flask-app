import os
import pytest
import sqlite3
from passenger_wsgi import create_app
from config import get_config

base_dir = os.path.dirname(__file__)
test_db = os.getenv("TEST_SQLITE_PATH", "")


@pytest.fixture
def sut():
    """Setup controller for integrationtest

    env-variable FLASK_ENV is set to test in pytest.ini file. This makes
    test use test-database
    """
    app = create_app()

    files = ["./db/ddl.sql", "./test/db/insert.sql"]

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    for file in files:
        with open(file, "r") as f:
            sql_commands = f.read()
            cursor.executescript(sql_commands)

    conn.commit()
    conn.close()

    yield app

    os.remove(test_db)


@pytest.fixture()
def client(sut):
    return sut.test_client()


@pytest.fixture()
def runner(sut):
    return sut.test_cli_runner()


@pytest.mark.scenario
def test_login_create_and_update_topic(client):
    login_response = client.post(
        "/api/users/login", json={"username": "admin", "password": "dosen't matter"}
    )
    jwt = login_response.json["data"]["jwt"]

    topic_response = client.post(
        "/api/topics",
        json={"title": "New things happening", "category": 15},
        headers={"Authorization": f"Bearer {jwt}"},
    )

    topic_id = topic_response.json["data"]["topic_id"]
    client.put(
        f"/api/topics/{topic_id}",
        json={"title": "Updated topic"},
        headers={"Authorization": f"Bearer {jwt}"},
    )

    get_updated_from_route = client.get(f"/api/topics/{topic_id}")

    topic = get_updated_from_route.json

    assert topic["data"]["title"] == "Updated topic"
