import socket
from datetime import datetime

MAX_BYTES = 65535

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        text = f"Il est {datetime.now()}"
        data = text.encode('utf-8')

        self.sock.sendto(data, (self.host, self.port))
        print(f"Mon adresse est {self.sock.getsockname()}")

        data, address = self.sock.recvfrom(MAX_BYTES)
        text = data.decode('utf-8')
        print(f"Le serveur dit : {text}")


if __name__ == "__main__":
    client = Client('127.0.0.1', 1060)
    client.start()