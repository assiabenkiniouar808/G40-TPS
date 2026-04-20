import socket

class LeChat:
    def __init__(self, max_client, max_message_len, ip_address, port):
        self.max_client = max_client
        self.max_message_len = max_message_len
        self.ip_address = ip_address
        self.port = port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip_address, self.port))
        self.server_socket.listen(self.max_client)

        self.clients = {}
        self.next_client_id = 0

        self.total_notes = 0
        self.nb_notes = 0

    def send(self, client_socket, message):
        client_socket.send(message.encode())

    def handle_llm(self, tokens):
        return f"Réponse du LLM pour les tokens : {tokens}"

    def manage_connexions(self):
        while True:
            client_socket, client_address = self.server_socket.accept()

            if len(self.clients) >= self.max_client:
                self.send(client_socket, "Serveur saturé")
                client_socket.close()
                continue

            client_id = self.next_client_id
            self.clients[client_id] = client_socket
            self.next_client_id += 1

            print(f"Client {client_id} connecté depuis {client_address}")

    def tokenizer(self, message, vocab):
        mots = message.split()
        tokens = []

        for mot in mots:
            if mot in vocab:
                tokens.append(vocab[mot])

        return tokens

    def handle_client(self, client_id, vocab):
        client_socket = self.clients[client_id]

        while True:
            message = client_socket.recv(1024).decode().strip()

            if (
                not message.endswith("?")
                or len(message) > self.max_message_len
                or "merci" in message.lower()
            ):
                self.send(client_socket, "Texte invalide")
                continue

            tokens = self.tokenizer(message, vocab)
            reponse = self.handle_llm(tokens)
            self.send(client_socket, reponse)

            note_str = client_socket.recv(1024).decode().strip()

            try:
                note = int(note_str)
                if 0 <= note <= 10:
                    self.total_notes += note
                    self.nb_notes += 1
                else:
                    self.send(client_socket, "Note invalide")
            except ValueError:
                self.send(client_socket, "Note invalide")

    def get_evaluation(self):
        if self.nb_notes == 0:
            return 0
        return self.total_notes / self.nb_notes