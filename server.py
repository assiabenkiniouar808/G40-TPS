import socket

MAX_BYTES = 65535

def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', port))
    print(f"Serveur en écoute sur {sock.getsockname()}")
    while True:
       
        data, address = sock.recvfrom(MAX_BYTES)

        text = data.decode('utf-8')
        print(f"Client {address} : {text}")

       
        reponse = f"Reçu : {len(data)} octets"
        data = reponse.encode('utf-8')

        sock.sendto(data, address)

if __name__ == "__main__":
    server(1060)