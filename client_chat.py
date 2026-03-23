import socket
import threading

MAX_BYTES = 65535

def recevoir(sock):
    while True:
        try:
            data, address = sock.recvfrom(MAX_BYTES)
            print("\nMessage reçu :", data.decode('utf-8'))
        except:
            break

def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    thread_reception = threading.Thread(target=recevoir, args=(sock,), daemon=True)
    thread_reception.start()

    print("Tape tes messages. Tape 'quit' pour quitter.")

    while True:
        text = input("> ")

        if text.lower() == "quit":
            break

        sock.sendto(text.encode('utf-8'), ('127.0.0.1', port))

    sock.close()

if __name__ == "__main__":
    client(1060)