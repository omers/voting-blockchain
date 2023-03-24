from bcb_server.orderer import app
import pytest
import json


@pytest.fixture(scope="session")
def client():
    app.config.update({"TESTING": True})
    return app.test_client()

def test_health_check_endpoint(client):
    response = client.get("/health")
    assert 200
    assert response.json == {"status": "ok"}

def test_add_node_endpoint_accept_only_post(client):
    response = client.open(
        "/add_node", method="OPTIONS"
    )
    assert sorted(response.allow) == ["OPTIONS", "POST"]
    assert response.data == b""

def test_add_node_endpoint(client):
    data = {"ipaddress": "192.68.1.1", "port": 5000}
    response = client.post(
        "/add_node", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201
    assert response.text == "Success"


def test_add_node_not_accepts_bad_ipaddress(client):
    data = {"ipaddress": "192.68.1", "port": 5000}
    response = client.post(
        "/add_node", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 400


def test_add_node_not_accepts_bad_ports_number(client):
    data = {"ipaddress": "192.68.1", "port": 1023}
    response = client.post(
        "/add_node", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 400


def test_add_node_not_accepts_bad_ports_type(client):
    data = {"ipaddress": "192.68.1", "port": "1023"}
    response = client.post(
        "/add_node", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 400


def test_broadcast_block_endpoint(client):
    pass
