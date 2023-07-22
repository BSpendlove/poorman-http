from socket import socket
from poorman_http.helpers import VALID_OPERATIONS
from poorman_http.response import HTTPResponse


class HTTPRequest:
    def __init__(
        self, operation: str, resource: str, sock: socket, headers: dict = {}
    ) -> None:
        self.version = "HTTP/1.1"
        self.operation = operation.upper()
        if self.operation not in VALID_OPERATIONS:
            raise ValueError(f"Operation {self.operation} is not a valid operation")

        self.resource = resource
        self._sock = sock
        self.headers = headers
        self._buffer = [self.build_start_line()]
        self.add_headers()

    def encode(self, data: str) -> str:
        """Adds return carriage to the data"""
        data = data.rstrip()  # Strip existing return carriages
        return data + "\r\n"

    def build_start_line(self) -> str:
        """Adds the start line to the buffer as per RFC7230 Section 3.1"""
        start_line = f"{self.operation} {self.resource} {self.version}"
        return self.encode(start_line)

    def queue(self, data) -> None:
        """Adds data to the local buffer"""
        self._buffer.append(data)

    def add_headers(self) -> None:
        """Adds headers to the buffer"""
        for k, v in self.headers.items():
            self._buffer.append(self.encode(f"{k}: {v}"))

    def send(self) -> HTTPResponse:
        """Send all existing data in the buffer to the socket

        Args:
            data:       Bytes of data
        """
        data = "".join(self._buffer).encode("ascii") + b"\r\n"
        self._sock.sendall(data)

        # Get Response
        res = HTTPResponse(sock=self._sock)

        self._buffer = [self.build_start_line()]
        self.add_headers()

        return res
