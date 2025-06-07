from dnslib import DNSRecord
import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8053
DOMAIN = "fmi.unibuc.r"

query = DNSRecord.question(DOMAIN)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)
sock.sendto(query.pack(), (SERVER_IP, SERVER_PORT))

try:
    data, _ = sock.recvfrom(512)
    response = DNSRecord.parse(data)
    answer = response.get_a()  
    if answer:
        ip = answer.rdata
        print(f"Test reușit: DNS clientul a primit un raspuns valid de la server — {DOMAIN} → {ip}. Aplicatia functioneaza corect.")
    else:
        print("Test esuat: Nu a fost primit niciun raspuns valid.")
except socket.timeout:
    print("Test esuat: Timeout — nu am primit niciun raspuns de la server.")
