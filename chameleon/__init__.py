import requests
import docker


class Chameleon:

    def __init__(self, server_uri='http://localhost:5000'):
        self.base_uri = server_uri

    def set_response(self, status_code, body, headers=None):
        """
        Set the response that the chameleon server will return.

        :param status_code: HTTP status code of the response
        :param body: response body
        :param headers: response HTTP headers
        """
        headers = headers or []
        payload = {
            'status_code': status_code,
            'body': body,
            'headers': headers,
        }
        requests.put(self.base_uri, json=payload, headers={'X-Chameleon': 'true'})

    def get_requests(self):
        """
        Retrieve the request that the Chameleon has received.

        :return: List of requests, e.g.:
        [
         {'args': [],
          'body': '',
          'cookies': {},
          'headers': [['Content-Length', ''],
           ['Connection', 'keep-alive'],
           ['Host', 'localhost:5000'],
           ['Accept', '*/*'],
          'method': 'GET',
          'path': '/abc',
          'url': 'http://localhost:5000/abc'
          }
        ]
        """
        r = requests.get(self.base_uri, headers={'X-Chameleon': 'true'})
        return r.json()

    def clear_requests(self):
        """
        Clears the list of requests received by the Chameleon server.

        (Next call to get_requests would return [] if nothing calls the server in between)
        """
        requests.delete(self.base_uri, headers={'X-Chameleon': 'true'})


class ChameleonServer:
    """
    Simple Docker wrapper to control the Chameleon server container.
    """

    def __init__(self, port=5000, version='latest'):
        self.image = 'jolleon/chameleon:{}'.format(version)
        self.port = port
        self.container = None

    def start(self):
        docker_client = docker.from_env()
        self.container = docker_client.containers.run(self.image, ports={'{}/tcp'.format(self.port): self.port}, detach=True)

    def stop(self):
        if self.container is not None:
            self.container.stop(timeout=0)

    def uri(self):
        return 'http://localhost:{}'.format(self.port)
