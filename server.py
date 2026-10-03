import os
import shared
import socket
from time import time
from threading import Thread
from json import dumps


class Server:
    def __init__(self):
        self.sock = shared.W2gSocket("192.168.101.104", 25565)
        self.clients: list[tuple[socket.socket, str]] = []

        self.sock.initServer()

    def handle(self, connection_data: tuple[socket.socket, socket._RetAddress]):
        id = str(connection_data[1][1])
        print(f"client {id} {connection_data[1]} connected")

        sock = connection_data[0]
        self.clients.append((sock, id))

        while True:
            d = shared.customRecv(sock)

            match d["op"]:
                case 0:
                    self.send_video(sock)
                case _:
                    shared.customSend(sock, {"op": 30, "d": f"unknown op {d['op']}"})
                    print(f"client {id} send invalid data")

    def send_video(self, sock: socket.socket):
        size = os.path.getsize("server/video.mp4")
        video = shared.Download("files/video.mp4", size)

        shared.customSend(sock, {"op": 1, "d": dumps(video, default=vars)})

        with open("server/video.mp4", "rb") as f:
            shared.customSendRaw(sock, f.read())

    def listen(self):
        try:
            while True:
                Thread(
                    target=self.handle,
                    args=(self.sock.accept(),),
                    daemon=True,
                ).start()
        except KeyboardInterrupt:
            self.sock.close()


server = Server()
server.listen()
