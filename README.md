# Chameleon

Chameleon is a mock server that will respond to any request with a predetermined response. It is configured over HTTP, records all requests received and can return them in JSON format.

## Quick Setup

```
# get the code
git clone git@github.com:jolleon/chameleon.git

# setup virtualenv
cd chameleon
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# run it!
CHAMELEON_PORT=8080 python chameleon.py
```

## Usage

In order to communicate with chameleon itself (and not hit the mock endpoint), set the `X-Chameleon` header (e.g. `X-Chameleon: true`).

With the `X-Chameleon` header set, you can:
- GET: retrieve the list of requests received by chameleon on the mock endpoint
- PUT: set a new response to return to all subsequent requests
- DELETE: erase the list of stored requests

Format for setting a response:
```
{
    "body": "response body goes here",
    "status_code": 200,
    "headers": [
        ["Content-Type", "application/json"],
        ["My-Header", "myvalue"]
    ]
}
```

## Examples

### Set a response using PUT
```
curl localhost:5001 -H "X-Chameleon: true" -X PUT -d '{"body": "abcd", "status_code": 200, "headers":[["Content-Type", "application/json"], ["My-Header", "myvalue"]]}'
```
(now try to query it *without* the `X-Chameleon` header)


### Retrieve stored requests with GET
```
curl localhost:5001 -H "X-Chameleon: true"
``` 

### Clear stored requests with DELETE
```
curl localhost:5001 -H "X-Chameleon: true" -X DELETE
```
