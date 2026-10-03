import os
import json
import socket
import typing


class Download:
    def __init__(self, filename, size, update=False):
        self.filename = filename
        self.size = size

        if not os.path.exists("files"):
            os.mkdir("files")

        if update:
            open(self.filename, "wb").close()

    def write(self, d):
        with open(self.filename, "ab") as f:
            f.write(d)


class W2gSocket:
    def __init__(self, ip, port, max_clients=10):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.max_clients = max_clients
        self.initialized = False

    def initServer(self):
        if self.initialized:
            return False

        self.sock.bind((self.ip, self.port))
        self.listen()
        self.initialized = True

    def initClient(self):
        if self.initialized:
            return False

        self.sock.connect((self.ip, self.port))
        self.initialized = True

    def listen(self):
        self.sock.listen(self.max_clients)

    def accept(self) -> tuple[socket.socket, typing.Any]:
        return self.sock.accept()

    def send(self, d: dict, log=True):
        if log:
            print(f"send: {d}")

        self.sock.send(json.dumps(d).encode())

    def recv(self, s=4096, log=True) -> dict:
        d = json.loads(self.sock.recv(s).decode())

        if log:
            print(f"recv: {d}")

        return d

    def send_raw(self, d: bytes, log=True):
        if log:
            print(f"send raw: {len(d) / 1000000}MB")

        self.sock.send(d)

    def recv_raw(self, s=4096, log=True) -> bytes:
        d = self.sock.recv(s)

        if log:
            print(f"recv raw: {len(d)}B")

        return d

    def close(self):
        self.sock.close()


def customSend(sock: socket.socket, d: dict, log=True):
    if log:
        print(f"custom send: {d}")

    sock.send(json.dumps(d).encode())


def customRecv(sock: socket.socket, s=4096, log=True) -> dict:
    d = json.loads(sock.recv(s).decode())

    if log:
        print(f"custom recv: {d}")

    return d


def customSendRaw(sock: socket.socket, d: bytes, log=True):
    if log:
        print(f"custom send raw: {len(d) / 1000000}MB")

    sock.send(d)


def customRecvRaw(sock: socket.socket, s=4096, log=True) -> bytes:
    d = sock.recv(s)

    if log:
        print(f"custom recv raw: {len(d)}B")

    return d
