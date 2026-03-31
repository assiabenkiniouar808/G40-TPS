import socket
from struct import pack

def checksum(data):
    s = 0

    if len(data) % 2 != 0:
        data += b'\x00'

    for i in range(0, len(data), 2):
        w = (data[i] << 8) + data[i + 1]
        s += w

    s = (s >> 16) + (s & 0xffff)
    s += (s >> 16)
    s = ~s & 0xffff

    return s

def create_ip_header(ip_source, ip_dest):
    ip_version = 4
    ip_ihl = 5
    ip_tos = 0
    ip_tot_len = 0
    ip_id = 54321
    ip_frag_off = 0
    ip_ttl = 255
    ip_proto = socket.IPPROTO_TCP
    ip_check = 0
    ip_saddr = socket.inet_aton(ip_source)
    ip_daddr = socket.inet_aton(ip_dest)

    ip_ihl_ver = (ip_version << 4) + ip_ihl

    ip_header = pack(
        '!BBHHHBBH4s4s',
        ip_ihl_ver,
        ip_tos,
        ip_tot_len,
        ip_id,
        ip_frag_off,
        ip_ttl,
        ip_proto,
        ip_check,
        ip_saddr,
        ip_daddr
    )

    return ip_header

def create_tcp_header(message, ip_source, ip_dest):
    tcp_source = 1234
    tcp_dest = 80
    tcp_seq = 454
    tcp_ack_seq = 0
    tcp_doff = 5

    tcp_fin = 0
    tcp_syn = 1
    tcp_rst = 0
    tcp_psh = 0
    tcp_ack = 0
    tcp_urg = 0

    tcp_window = socket.htons(5840)
    tcp_check = 0
    tcp_urg_ptr = 0

    tcp_offset_res = (tcp_doff << 4) + 0
    tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)

    tcp_header = pack(
        '!HHLLBBHHH',
        tcp_source,
        tcp_dest,
        tcp_seq,
        tcp_ack_seq,
        tcp_offset_res,
        tcp_flags,
        tcp_window,
        tcp_check,
        tcp_urg_ptr
    )

    source_address = socket.inet_aton(ip_source)
    dest_address = socket.inet_aton(ip_dest)
    placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(tcp_header) + len(message.encode())

    psh = pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
    psh = psh + tcp_header + message.encode()

    tcp_check = checksum(psh)

    tcp_header = pack(
        '!HHLLBBH',
        tcp_source,
        tcp_dest,
        tcp_seq,
        tcp_ack_seq,
        tcp_offset_res,
        tcp_flags,
        tcp_window
    ) + pack('!H', tcp_check) + pack('!H', tcp_urg_ptr)

    return tcp_header

def create_packet(ip_header, tcp_header, message):
    return ip_header + tcp_header + message.encode()

if __name__ == '__main__':
    ip_source = '127.0.0.1'
    ip_dest = '127.0.0.1'
    message = input("Entrez le message à envoyer : ")

    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

    ip_header = create_ip_header(ip_source, ip_dest)
    tcp_header = create_tcp_header(message, ip_source, ip_dest)
    packet = create_packet(ip_header, tcp_header, message)

    s.sendto(packet, (ip_dest, 0))
    print("Paquet envoyé.")
