import time
import docker
import pytest
import requests

from chameleon_client import client


@pytest.fixture
def chameleon_server():
    docker_client = docker.from_env()
    container = docker_client.containers.run('jolleon/chameleon:latest', ports={'5000/tcp': 5000}, detach=True)
    time.sleep(1)
    yield container
    container.stop(timeout=1)


def test_client(chameleon_server):
    c = client.Chameleon()
    r = c.get_requests()
    assert r == []

    r = requests.get('http://localhost:5000/abc')
    assert r.status_code == 400

    payload = {"a": {"b": "cc", "dd": 2}}
    c.set_response(200, payload)

    r = requests.get('http://localhost:5000/abc')
    assert r.status_code == 200
    assert r.json() == payload

    r = c.get_requests()
    assert len(r) == 1
    assert r[0]['path'] == '/abc'

    r = requests.get('http://localhost:5000/bcd', headers={'X-Blah': 'something'})
    assert r.status_code == 200
    assert r.json() == payload

    r = c.get_requests()
    assert len(r) == 2
    assert r[0]['path'] == '/abc'
    assert r[1]['path'] == '/bcd'
    assert ['X-Blah', 'something'] in r[1]['headers']