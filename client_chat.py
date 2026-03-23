import socket

MAX_BYTES = 65535

def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        text = input('Votre message : ')
        data = text.encode('ascii')
        sock.sendto(data, ('127.0.0.1', port))
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        print('Message recu : {}'.format(text))

if _name_ == '_main_':
    client(1060)
