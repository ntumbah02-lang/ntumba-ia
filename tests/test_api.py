"""Minimal tests placeholder."""

from fastapi.testclient import TestClient
from server.main import app


def test_root_serves_index():
    client = TestClient(app)
    res = client.get('/')
    assert res.status_code == 200


def test_chat_requires_message():
    client = TestClient(app)
    res = client.post('/api/chat', json={})
    assert res.status_code == 422 or res.status_code == 400
