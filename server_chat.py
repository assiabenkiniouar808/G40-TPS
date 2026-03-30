import socket

MAX_BYTES = 65535

def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', port))
    print('En ecoute sur {}'.format(sock.getsockname()))
    
    clients = []  
    
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        print('Le client {} dit {!r}'.format(address, text))
        
        if address not in clients:
            clients.append(address)
        for client in clients:
            if client != address:
                sock.sendto(data, client)

if _name_ == '_main_':
    server(1060)
