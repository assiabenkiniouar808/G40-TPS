import socket
from _thread import start_new_thread
import threading
import struct
import json

class Serveur:
    def __init__(self, host="127.0.0.1", port=80):
        self.host = host
        self.port = port
        self.print_lock = threading.Lock()
        self.clients = {}

    def envoyer_json(self, c, message):
        pass  

    def diffuser(self, message, exclure_socket=None):
        pass  

    def envoyer_nombre_clients(self):
        message = {
            "type": "notification",
            "evenement": "nb_clients",
            "nombre": len(self.clients)
        }
        print(json.dumps(message, ensure_ascii=False))

    def parse_ip_header(self, data):
        ip_header = data[0:20]
        iph = struct.unpack('!BBHHHBBH4s4s', ip_header)

        version_ihl = iph[0]
        ihl = version_ihl & 0xF
        ip_header_length = ihl * 4

        protocol = iph[6]
        source_ip = socket.inet_ntoa(iph[8])
        dest_ip = socket.inet_ntoa(iph[9])

        return {
            "ip_header_length": ip_header_length,
            "protocol": protocol,
            "source_ip": source_ip,
            "dest_ip": dest_ip
        }

    def parse_tcp_header(self, data, ip_header_length):
        tcp_start = ip_header_length
        tcp_header = data[tcp_start:tcp_start + 20]

        tcph = struct.unpack('!HHLLBBHHH', tcp_header)

        source_port = tcph[0]
        dest_port = tcph[1]
        offset_reserved = tcph[4]
        tcp_header_length = (offset_reserved >> 4) * 4

        return {
            "source_port": source_port,
            "dest_port": dest_port,
            "tcp_header_length": tcp_header_length
        }

    def communication_client(self, packet):
        try:
            if len(packet) < 40:
                return

            ip_info = self.parse_ip_header(packet)

            if ip_info["protocol"] != socket.IPPROTO_TCP:
                return

            tcp_info = self.parse_tcp_header(packet, ip_info["ip_header_length"])

            if tcp_info["dest_port"] != self.port:
                return

            data_start = ip_info["ip_header_length"] + tcp_info["tcp_header_length"]
            payload = packet[data_start:]

            if not payload:
                return

            message = payload.decode(errors="ignore").strip()

            client_id = (ip_info["source_ip"], tcp_info["source_port"])
            nom = f"{ip_info['source_ip']}:{tcp_info['source_port']}"

            with self.print_lock:
                if client_id not in self.clients:
                    self.clients[client_id] = nom
                    print(f"{nom} s'est connecté.")
                    self.envoyer_nombre_clients()

            print("\n----- Message reçu -----")
            print("Source :", nom)
            print("Message :", message)
            print("------------------------")

        except Exception as e:
            print("Erreur :", e)

    def thread_ecoute(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

        

        print("Serveur raw en écoute...")

        while True:
            packet, addr = s.recvfrom(65535)
            start_new_thread(self.communication_client, (packet,))

if __name__ == '__main__':
    serveur = Serveur()
    serveur.thread_ecoute()