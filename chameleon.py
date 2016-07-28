import os
import json
from flask import Flask, request, make_response
from werkzeug.routing import Rule

app = Flask(__name__)
app.url_map.add(Rule('/', endpoint='index', defaults={'path': ''}))
app.url_map.add(Rule('/<path:path>', endpoint='index'))

response = None
received_requests = []

USAGE = """Chameleon is a mock server that will respond to any request with a predetermined response. It is configured using HTTP by setting the X-Chameleon header (e.g. "X-Chameleon: true").

    Set a response using PUT:
        curl localhost:5000 -H "X-Chameleon: true" -X PUT -d '{"body": "abcd", "status_code": 200, "headers":[["Content-Type", "application/json"], ["My-Header", "myvalue"]]}'

    Retrieve stored requests with GET:
        curl localhost:5000 -H "X-Chameleon: true"

    Reset stored requests with DELETE:
        curl localhost:5000 -H "X-Chameleon: true" -X DELETE
"""
@app.endpoint('index')
def catch_all(path):
    global response, received_requests
    if request.headers.get('X-Chameleon'):
        if request.method == 'PUT':
            response = request.get_json(force=True)
            return 'response set', 200
        if request.method == 'GET':
            return json.dumps(received_requests)
        if request.method == 'DELETE':
            received_requests = []
            return 'memory wiped', 200
        return USAGE, 400

    if response is None:
        return "Error: no response configured!\n\n" + USAGE, 400

    last_request = {}
    last_request['method'] = request.method
    last_request['path'] = request.path
    last_request['url'] = request.url
    last_request['args'] = request.args.items()
    last_request['headers'] = request.headers.items()
    last_request['cookies'] = request.cookies
    last_request['body'] = request.form
    received_requests.append(last_request)

    resp = make_response(response['body'], response['status_code'])
    for k, v in response.get('headers', []):
        resp.headers[k] = v
    return resp

if __name__ == '__main__':
    host = os.environ.get("CHAMELEON_HOST", '0.0.0.0')
    port = os.environ.get("CHAMELEON_PORT", 5001)
    app.run(host=host, port=port)
