from typing import Tuple
from socket import socket
import json


class HTTPResponse:
    def __init__(self, sock: socket):
        self.fp = sock.makefile("rb")
        self.version = None
        self.status_code = None
        self.reason = None
        self.text = None
        self.headers = {}

        self.decode_response()

    def json(self) -> dict:
        if not self.headers.get("content-type"):
            return None

        if "application/json" not in self.headers["content-type"]:
            raise ValueError("application/json is not a valid content-type")

        try:
            json_data = json.loads(self.text)
        except Exception as err:
            raise err

        return json_data

    def decode_response(self):
        self.read_status_line()
        self.read_headers()
        self.read_data()

    def read_status_line(self) -> Tuple[str, int, str]:
        """Reads the initial HTTP response"""
        line = self.fp.readline()
        version, status_code, textual_phrase = line.split(maxsplit=3)

        self.version = version
        self.status_code = status_code
        self.reason = textual_phrase

    def read_headers(self) -> None:
        """Reads headers from the Response"""
        while True:
            line = self.fp.readline()
            if line in (b"\r\n", b"\n", b""):
                break

            header = line.decode(
                "iso-8859-1"
            )  # https://datatracker.ietf.org/doc/html/rfc7230#section-3.2.4
            k, v = header.split(":", 1)
            v = v.rstrip()
            if k in self.headers:
                print("dingdong")
                self.headers[k] = f"{self.headers[k]},{v}"
                continue

            self.headers[k] = v

    def read_data(self) -> None:
        """Reads the data from the Response"""
        self.text = self.fp.readline()
