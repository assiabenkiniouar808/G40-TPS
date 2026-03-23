import socket

MAX_BYTES = 65535

def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', port))

    print(f"Serveur en écoute sur {sock.getsockname()}")

    clients = []

    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('utf-8')

        if address not in clients:
            clients.append(address)
            print(f"Nouveau client enregistré : {address}")

        print(f"Message reçu de {address} : {text}")

        for client in clients:
            if client != address:
                message = f"{address} dit : {text}"
                sock.sendto(message.encode('utf-8'), client)