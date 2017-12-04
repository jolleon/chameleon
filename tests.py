import time
import docker
import pytest
import requests

from chameleon import Chameleon


@pytest.fixture(scope='session')
def chameleon_server():
    docker_client = docker.from_env()
    container = docker_client.containers.run('jolleon/chameleon:latest', ports={'5000/tcp': 5000}, detach=True)
    time.sleep(1)
    yield 'http://localhost:5000'
    container.stop(timeout=0)


def test_new_server(chameleon_server):
    c = Chameleon()
    r = c.get_requests()
    assert r == []

    r = requests.get('{}/abc'.format(chameleon_server))
    assert r.status_code == 400


@pytest.mark.parametrize('payload', [
    "my response",
    "{1: 2}",
    '{"a": {"b": "cc", "dd": 2}}',
])
def test_client(chameleon_server, payload):
    c = Chameleon()
    c.clear_requests()
    c.set_response(200, payload)

    r = requests.get('{}/abc'.format(chameleon_server))
    assert r.status_code == 200
    assert r.content.decode() == payload

    r = c.get_requests()
    assert len(r) == 1
    assert r[0]['path'] == '/abc'

    r = requests.get('{}/bcd'.format(chameleon_server), headers={'X-Blah': 'something'})
    assert r.status_code == 200
    assert r.content.decode() == payload

    r = c.get_requests()
    assert len(r) == 2
    assert r[0]['path'] == '/abc'
    assert r[1]['path'] == '/bcd'
    assert ['X-Blah', 'something'] in r[1]['headers']


@pytest.mark.parametrize('payload', [
    {"a": {"b": "cc", "dd": 2}},
])
def test_client_json(chameleon_server, payload):
    c = Chameleon()
    c.clear_requests()
    c.set_response(200, payload)

    r = requests.get('{}/abc'.format(chameleon_server))
    assert r.status_code == 200
    assert r.json() == payload

    r = c.get_requests()
    assert len(r) == 1
    assert r[0]['path'] == '/abc'

    r = requests.get('{}/bcd'.format(chameleon_server), headers={'X-Blah': 'something'})
    assert r.status_code == 200
    assert r.json() == payload

    r = c.get_requests()
    assert len(r) == 2
    assert r[0]['path'] == '/abc'
    assert r[1]['path'] == '/bcd'
    assert ['X-Blah', 'something'] in r[1]['headers']