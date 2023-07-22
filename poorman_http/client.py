from typing import Any
import socket
import traceback
from poorman_http.request import HTTPRequest
from poorman_http.response import HTTPResponse


class HTTPClient:
    def __init__(self, host: str, port: int = 80, headers: dict = {}) -> None:
        self.host = host
        self.port = port
        self.headers = headers

        self._socket = None

    def __enter__(self):
        self.setup_socket()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)

        if not self._socket:
            return

        self._socket.close()

    def setup_socket(self) -> None:
        """Sets up the initial socket to send HTTP data over"""
        socket_info = socket.getaddrinfo(
            host=self.host,
            port=self.port,
            family=socket.AF_INET,
            proto=socket.IPPROTO_TCP,
        )
        if len(socket_info) == 0:
            raise Exception("bimbom")

        family, socket_type, proto, canonname, sockaddr = socket_info[0]
        self._socket = socket.create_connection(address=sockaddr)

    def get(self, endpoint: str, params: dict = {}) -> HTTPResponse:
        """Implements basic HTTP GET operation

        Args:
            url:        URL Path
            params:     Dictionary of query params to add to the URL
        """
        req = HTTPRequest(
            operation="GET", resource=endpoint, sock=self._socket, headers=self.headers
        )
        response = req.send()
        return response

    def put() -> Any:
        raise NotImplementedError()

    def post() -> Any:
        raise NotImplementedError()

    def patch() -> Any:
        raise NotImplementedError()

    def delete() -> Any:
        raise NotImplementedError()
