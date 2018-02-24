import time
import pytest
import requests

from chameleon import ChameleonServer


@pytest.fixture(scope='session')
def chameleon_server():
    server = ChameleonServer(5000)
    time.sleep(1)
    yield server
    server.stop()


@pytest.fixture
def chameleon(chameleon_server):
    client = chameleon_server.make_client()
    client.clear_requests()
    return client


def test_new_server(chameleon):
    r = chameleon.get_requests()
    assert r == []

    r = requests.get('{}/abc'.format(chameleon.base_uri))
    assert r.status_code == 400


@pytest.mark.parametrize('payload', [
    "my response",
    "{1: 2}",
    '{"a": {"b": "cc", "dd": 2}}',
    '"abc"',
])
def test_text(chameleon, payload):
    chameleon.set_response(200, payload)

    r = requests.get('{}/abc'.format(chameleon.base_uri))
    assert r.status_code == 200
    assert r.content.decode() == payload

    r = chameleon.get_requests()
    assert len(r) == 1
    assert r[0]['path'] == '/abc'

    r = requests.get('{}/bcd'.format(chameleon.base_uri), headers={'X-Blah': 'something'})
    assert r.status_code == 200
    assert r.content.decode() == payload

    r = chameleon.get_requests()
    assert len(r) == 2
    assert r[0]['path'] == '/abc'
    assert r[1]['path'] == '/bcd'
    assert ['X-Blah', 'something'] in r[1]['headers']


@pytest.mark.parametrize('payload, parsed_response', [
    ({"a": {"b": "cc", "dd": 2}}, {"a": {"b": "cc", "dd": 2}}),
    ('{"a": {"b": "cc", "dd": 2}}', {"a": {"b": "cc", "dd": 2}}),
    ('"abc"', 'abc'),
])
def test_json(chameleon, payload, parsed_response):
    chameleon.set_response(200, payload)

    r = requests.get('{}/abc'.format(chameleon.base_uri))
    assert r.status_code == 200
    assert r.json() == parsed_response

    r = chameleon.get_requests()
    assert len(r) == 1
    assert r[0]['path'] == '/abc'

    r = requests.get('{}/bcd'.format(chameleon.base_uri), headers={'X-Blah': 'something'})
    assert r.status_code == 200
    assert r.json() == parsed_response

    r = chameleon.get_requests()
    assert len(r) == 2
    assert r[0]['path'] == '/abc'
    assert r[1]['path'] == '/bcd'
    assert ['X-Blah', 'something'] in r[1]['headers']