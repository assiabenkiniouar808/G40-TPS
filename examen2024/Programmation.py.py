import socket
import threading


class Game(object):
    def __init__(self, host, port, max_gamers, nbr_sticks):
        self.host = host
        self.port = port
        self.max_gamers = max_gamers          # nombre maximal de joueurs
        self.nbr_sticks = nbr_sticks          # nombre de bâtonnets restants
        self.players = []                     # liste des sockets clients connectés
        self.server_socket = None
        self.lock = threading.Lock()          # protège l'état partagé du jeu
        self.game_over = False

    def send(self, client_socket, message):
        try:
            client_socket.sendall((message + "\n").encode())
        except:
            pass

    def read(self, client_socket):
        try:
            data = client_socket.recv(1024).decode().strip()
            return data
        except:
            return ""

    def broadcast(self, message, except_client=None):
        for player in self.players:
            if player != except_client:
                self.send(player, message)

    def remove_player(self, client_socket):
        if client_socket in self.players:
            self.players.remove(client_socket)
        try:
            client_socket.close()
        except:
            pass

    def listen(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.max_gamers)

        print(f"Serveur lancé sur {self.host}:{self.port}")
        print("En attente de connexions...")

        while len(self.players) < self.max_gamers:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connexion acceptée depuis {client_address}")

            if len(self.players) >= self.max_gamers:
                self.send(client_socket, "Serveur plein")
                client_socket.close()
            else:
                self.players.append(client_socket)
                self.send(client_socket, "Connexion acceptée au jeu")

        print("Nombre maximal de joueurs atteint. Début du jeu.")

    def communicate_with_client(self, client_socket):
        while not self.game_over:
            with self.lock:
                if self.game_over:
                    break

                
                self.send(
                    client_socket,
                    f"Il reste {self.nbr_sticks} bâtonnets. "
                    f"Choisissez 1, 2 ou 3 bâtonnets à retirer"
                )

            msg = self.read(client_socket)

            with self.lock:
                if self.game_over:
                    break

                
                if not msg.isdigit():
                    self.send(client_socket, "Erreur : vous devez envoyer un chiffre")
                    continue

                n = int(msg)

                
                if n < 1 or n > 3:
                    self.send(client_socket, "Erreur : choisissez 1, 2 ou 3")
                    continue

                
                if n > self.nbr_sticks:
                    self.send(client_socket, "Erreur : pas assez de bâtonnets restants")
                    continue

                
                self.nbr_sticks -= n

               
                if self.nbr_sticks > 0:
                    self.send(client_socket, "Vous restez dans le jeu")
                    self.broadcast(
                        f"Un joueur a retiré {n} bâtonnet(s). "
                        f"Il reste {self.nbr_sticks} bâtonnets."
                    )
                else:
                    
                    self.send(client_socket, "Perdu")
                    self.broadcast("Gagné", except_client=client_socket)
                    self.game_over = True

        try:
            client_socket.close()
        except:
            pass

    def start(self):
        self.listen()

        threads = []
        for player in self.players:
            t = threading.Thread(target=self.communicate_with_client, args=(player,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        print("Jeu terminé.")
        self.server_socket.close()


if __name__ == "__main__":
    game = Game(host="127.0.0.1", port=5000, max_gamers=2, nbr_sticks=10)
    game.start()