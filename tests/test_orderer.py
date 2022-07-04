from bcb_server.orderer import app
import pytest
import json


@pytest.fixture()
def client():
    app.config.update({"TESTING": True})
    return app.test_client()


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
