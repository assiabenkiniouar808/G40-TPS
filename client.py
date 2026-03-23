import socket
from datetime import datetime

MAX_BYTES = 65535

def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Message envoyé
    text = f"Il est {datetime.now()}"
    data = text.encode('utf-8')

    # Envoi au serveur
    sock.sendto(data, ('127.0.0.1', port))

    print(f"Mon adresse est {sock.getsockname()}")

    # Réception de la réponse
    data, address = sock.recvfrom(MAX_BYTES)
    text = data.decode('utf-8')

    print(f"Le serveur dit : {text}")

if __name__ == "__main__":
    client(1060)