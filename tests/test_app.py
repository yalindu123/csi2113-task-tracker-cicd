import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import app, tasks


@pytest.fixture
def client():
    app.config["TESTING"] = True
    tasks.clear()
    with app.test_client() as client:
        yield client


def test_index_loads(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Task Tracker" in resp.data


def test_health_endpoint(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_add_task(client):
    client.post("/add", data={"title": "Write CI/CD pipeline"})
    resp = client.get("/api/tasks")
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Write CI/CD pipeline"


def test_complete_task(client):
    client.post("/add", data={"title": "Test task"})
    task_id = client.get("/api/tasks").get_json()[0]["id"]
    client.post(f"/complete/{task_id}")
    data = client.get("/api/tasks").get_json()
    assert data[0]["done"] is True


def test_delete_task(client):
    client.post("/add", data={"title": "Temp task"})
    task_id = client.get("/api/tasks").get_json()[0]["id"]
    client.post(f"/delete/{task_id}")
    data = client.get("/api/tasks").get_json()
    assert len(data) == 0


def test_add_empty_title_ignored(client):
    client.post("/add", data={"title": "   "})
    data = client.get("/api/tasks").get_json()
    assert len(data) == 0
