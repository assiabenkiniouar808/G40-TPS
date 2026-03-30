import socket
import threading
import json
from datetime import datetime

class Client:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
    
    def recevoir_messages(self, s):
        while True:
            try:
                data = s.recv(1024).decode()
                if not data:
                    break
                print(f"\n{data}")
            except:
                break

    def main(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))

        print(s.recv(1024).decode())

        nom = input("Entrez votre nom : ")
        lieu = input("Entrez votre lieu : ")
        date_connexion = datetime.now().strftime("%d/%m/%Y")

        # Message JSON
        message_json = {
            "nom": nom,
            "date_connexion": date_connexion,
            "lieu": lieu
        }

        s.send(json.dumps(message_json).encode())

        liste = s.recv(1024).decode()
        print(liste)

        print("Format pour envoyer : 'destinataire:message'")
        print("Tapez 'quit' pour quitter\n")

        thread = threading.Thread(target=self.recevoir_messages, args=(s,))
        thread.daemon = True
        thread.start()

        while True:
            message = input()
            if message.lower() == 'quit':
                s.send("quit".encode())
                break
            s.send(message.encode())

        s.close()

if __name__ == '__main__':
    client = Client()
    client.main()