import socket

MAX_BYTES = 65535

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def start(self):
        print(f"Serveur en écoute sur {self.sock.getsockname()}")

        while True:
            data, address = self.sock.recvfrom(MAX_BYTES)
            text = data.decode('utf-8')
            print(f"Client {address} : {text}")

            reponse = f"Reçu : {len(data)} octets"
            self.sock.sendto(reponse.encode('utf-8'), address)


if __name__ == "__main__":
    server = Server('127.0.0.1', 1060)
    server.start()