import asyncio
import os
import proxy
import shared
import socket
import typing
from time import time
from threading import Thread
from json import JSONDecodeError, dumps


class Client:
    def __init__(self, d: tuple[socket.socket, typing.Any]):
        self.sock = d[0]
        self.id = f"{d[1][0]}:{d[1][1]}"

        self.username = "Anonymous"
        self.avatar = ""
        self.prefix = f"[{self.id}]"

        print(f"client {self.id} connected")

    def handle(self):
        self.log("handling client")

        try:
            while True:
                d = shared.customRecv(self.sock)

                match d["op"]:
                    case 0:
                        self.send_video()
                    case 2:
                        pass
                    case _:
                        shared.customSend(
                            self.sock, {"op": 30, "d": f"unknown op {d['op']}"}
                        )
                        self.log("client send invalid data")
        except JSONDecodeError:
            self.log("disconnected")

    def send_video(self):
        size = os.path.getsize("server/video.mp4")
        video = shared.Download("files/video.mp4", size)

        shared.customSend(self.sock, {"op": 1, "d": dumps(video, default=vars)})

        with open("server/video.mp4", "rb") as f:
            shared.customSendRaw(self.sock, f.read())

    def log(self, text: str):
        print(f"{self.prefix} {text}")


class Server:
    def __init__(self):
        self.sock = shared.W2gSocket("192.168.101.104", 25565)
        self.clients: list[Client] = []

        self.sock.initServer()

    def listen(self):
        print("TCP server running")

        try:
            while True:
                Thread(
                    target=Client(self.sock.accept()).handle,
                    daemon=True,
                ).start()
        except KeyboardInterrupt:
            self.sock.close()


Thread(target=asyncio.run, args=(proxy.main(),), daemon=True).start()

server = Server()
server.listen()
