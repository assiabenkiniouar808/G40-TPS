import socket

def connect_to_google():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("maps.google.com", 80))

    requete = (
        "GET / HTTP/1.1\r\n"
        "Host: maps.google.com\r\n"
        "User-Agent: PythonSocketClient\r\n"
        "Connection: close\r\n"
        "\r\n"
    )

    sock.sendall(requete.encode())

    reponse = sock.recv(4096)
    print(reponse.decode(errors="ignore"))

    sock.close()

if __name__ == "__main__":
    connect_to_google()