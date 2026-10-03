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
        self.prefix = f"[{self.id}]:"

        print(f"client {self.id} connected")

    def handle(self):
        self.log("handling client")

        try:
            while True:
                d = shared.customRecv(self.sock)

                if not d:
                    break

                match d["op"]:
                    case 0:
                        self.send_video()
                    case 2:
                        self.auth(d["d"])
                    case _:
                        self.send_error(f"unknown op {d['op']}")
        except JSONDecodeError:
            self.log("invalid JSON payload")
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            self.log("unexpected network disconnection")
        except Exception as e:
            self.log(f"error (disconnected): {e}")

        self.log("connection loop end")

    def auth(self, d: dict):
        self.log("authorizing")

        if not "username" in d:
            self.send_error("invalid username (no username), auth failed")

            return

        if 3 > len(d["username"]) > 15:
            self.send_error("invalid username (too short or too long), auth failed")

            return

        self.username = d["username"]
        self.updatePrefix()

        for client in server.clients:
            shared.customSend(client.sock, {"op": 10, "d": {"username": self.username}})
            self.log(f"broadcasted to {client.username} ({client.id}) server join")

    def send_error(self, msg: str):
        shared.customSend(self.sock, {"op": 30, "d": "invalid username"})
        self.log(f"error: {msg}")

    def send_video(self):
        size = os.path.getsize("server/video.mp4")
        video = shared.Download("files/video.mp4", size)

        shared.customSend(self.sock, {"op": 1, "d": dumps(video, default=vars)})

        with open("server/video.mp4", "rb") as f:
            shared.customSendRaw(self.sock, f.read())

    def updatePrefix(self):
        self.prefix = f"[{self.id}] {self.username}:"
        self.log("updated prefix")

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
                self.clients.append(Client(self.sock.accept()))

                Thread(
                    target=self.clients[-1].handle,
                    daemon=True,
                ).start()
        except KeyboardInterrupt:
            self.sock.close()


Thread(target=asyncio.run, args=(proxy.main(),), daemon=True).start()

server = Server()
server.listen()
