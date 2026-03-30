import socket
from _thread import start_new_thread
import threading
import json

class Serveur:
    def __init__(self, host="", port=12345):
        self.host = host
        self.port = port
        self.print_lock = threading.Lock()
        self.clients = {}  # {socket: nom_client}

    def envoyer_json(self, c, message):
        c.send(json.dumps(message).encode())

    def diffuser(self, message, exclure_socket=None):
        for client_socket in list(self.clients.keys()):
            if client_socket != exclure_socket:
                try:
                    self.envoyer_json(client_socket, message)
                except:
                    pass

    def envoyer_nombre_clients(self):
        message = {
            "type": "notification",
            "evenement": "nb_clients",
            "nombre": len(self.clients)
        }
        self.diffuser(message)

    def communication_client(self, c):
        nom = None
        try:
            c.send("Connexion au serveur réussie.".encode())

            data = c.recv(1024).decode().strip()
            premier_message = json.loads(data)

            if premier_message["type"] != "identification":
                self.envoyer_json(c, {
                    "type": "erreur",
                    "contenu": "Le premier message doit être une identification."
                })
                c.close()
                return

            nom = premier_message["nom"]
            date_connexion = premier_message["date_connexion"]
            lieu = premier_message["lieu"]

            with self.print_lock:
                self.clients[c] = nom

            print(f"{nom} s'est connecté.")
            print(f"Date de connexion : {date_connexion}")
            print(f"Lieu de connexion : {lieu}")

            self.envoyer_nombre_clients()

            self.diffuser({
                "type": "notification",
                "evenement": "connexion",
                "nom": nom
            }, exclure_socket=c)

            while True:
                data = c.recv(1024)
                if not data:
                    break

                message = json.loads(data.decode())

                if message["type"] == "message":
                    destinataire = message["destinataire"]
                    contenu = message["contenu"]

                    envoye = False
                    for client_socket, client_nom in list(self.clients.items()):
                        if client_nom == destinataire:
                            self.envoyer_json(client_socket, {
                                "type": "message",
                                "source": nom,
                                "contenu": contenu
                            })
                            envoye = True
                            break

                    if not envoye:
                        self.envoyer_json(c, {
                            "type": "erreur",
                            "contenu": f"Client '{destinataire}' introuvable."
                        })

                elif message["type"] == "notification":
                    if message["evenement"] == "ecriture":
                        self.diffuser({
                            "type": "notification",
                            "evenement": "ecriture",
                            "nom": nom
                        }, exclure_socket=c)

                elif message["type"] == "etat":
                    self.diffuser({
                        "type": "etat",
                        "nom": nom,
                        "etat": message["etat"]
                    }, exclure_socket=c)

        except json.JSONDecodeError:
            print("Erreur : message JSON invalide.")
        except ConnectionResetError:
            print(f"Connexion coupée brutalement par {nom}.")
        except Exception as e:
            print(f"Erreur avec le client {nom} : {e}")
        finally:
            with self.print_lock:
                if c in self.clients:
                    nom_client = self.clients[c]
                    del self.clients[c]

                    self.diffuser({
                        "type": "notification",
                        "evenement": "deconnexion",
                        "nom": nom_client
                    }, exclure_socket=c)

                    self.envoyer_nombre_clients()
                    print(f"{nom_client} s'est déconnecté.")
            c.close()

    def thread_ecoute(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        print("Socket bindée au port", self.port)

        s.listen(5)
        print("Le serveur est en écoute...")

        while True:
            c, addr = s.accept()
            print("Connecté au client :", addr[0], ":", addr[1])
            start_new_thread(self.communication_client, (c,))

if __name__ == '__main__':
    serveur = Serveur()
    serveur.thread_ecoute()