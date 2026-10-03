import shared
from json import loads


class ClientDownload:
    def __init__(self, sock: shared.W2gSocket):
        self.sock = sock
        self.sock.send({"op": 0})

        d = sock.recv()

        self.download = shared.Download(**loads(d["d"]), update=True)

    def startDownload(self):
        size = 0

        while size < self.download.size:
            d = self.sock.recv_raw(8192, log=False)

            self.download.write(d)
            size += len(d)

            print(
                f"downloading file {(round((size / self.download.size) * 100, 2))}% {size}/{self.download.size}",
                end="\r",
            )

        print("\ndownload complete")


sock = shared.W2gSocket(input("ip: "), 25565)

sock.initClient()
ClientDownload(sock).startDownload()
sock.close()
