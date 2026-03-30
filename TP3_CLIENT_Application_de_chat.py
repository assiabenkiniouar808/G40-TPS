import socket
import threading
import json
from datetime import datetime

class Client:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.nom = ""

    def recevoir_messages(self, s):
        while True:
            try:
                data = s.recv(1024).decode()
                if not data:
                    break

                message = json.loads(data)

                if message["type"] == "notification":
                    if message["evenement"] == "nb_clients":
                        print(f"\n[Serveur] Nombre de clients connectés : {message['nombre']}")
                    elif message["evenement"] == "connexion":
                        print(f"\n[Notification] {message['nom']} s'est connecté.")
                    elif message["evenement"] == "deconnexion":
                        print(f"\n[Notification] {message['nom']} s'est déconnecté.")
                    elif message["evenement"] == "ecriture":
                        print(f"\n[Notification] {message['nom']} est en train d'écrire...")

                elif message["type"] == "etat":
                    print(f"\n[Etat] {message['nom']} est maintenant {message['etat']}")

                elif message["type"] == "message":
                    print(f"\n[{message['source']}] : {message['contenu']}")

                elif message["type"] == "erreur":
                    print(f"\n[Erreur] {message['contenu']}")

            except:
                break

    def main(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))

        print(s.recv(1024).decode())

        self.nom = input("Entrez votre nom : ")
        lieu = input("Entrez votre lieu : ")
        date_connexion = datetime.now().strftime("%d/%m/%Y")

        identification = {
            "type": "identification",
            "nom": self.nom,
            "date_connexion": date_connexion,
            "lieu": lieu
        }

        s.send(json.dumps(identification).encode())

        thread = threading.Thread(target=self.recevoir_messages, args=(s,))
        thread.daemon = True
        thread.start()

        print("\nCommandes :")
        print("1. message privé  -> msg:destinataire:contenu")
        print("2. changer état   -> etat:LIBRE")
        print("3. en train d'écrire -> ecriture")
        print("4. quitter -> quit\n")

        while True:
            texte = input()

            if texte.lower() == "quit":
                break

            elif texte.lower() == "ecriture":
                notif = {
                    "type": "notification",
                    "evenement": "ecriture",
                    "nom": self.nom
                }
                s.send(json.dumps(notif).encode())

            elif texte.startswith("etat:"):
                nouvel_etat = texte.split(":", 1)[1].strip().upper()
                msg_etat = {
                    "type": "etat",
                    "nom": self.nom,
                    "etat": nouvel_etat
                }
                s.send(json.dumps(msg_etat).encode())

            elif texte.startswith("msg:"):
                parties = texte.split(":", 2)
                if len(parties) == 3:
                    destinataire = parties[1].strip()
                    contenu = parties[2].strip()

                    msg = {
                        "type": "message",
                        "source": self.nom,
                        "destinataire": destinataire,
                        "contenu": contenu
                    }
                    s.send(json.dumps(msg).encode())
                else:
                    print("Format invalide. Utilisez msg:destinataire:contenu")

            else:
                print("Commande inconnue.")

        s.close()

if __name__ == '__main__':
    client = Client()
    client.main()