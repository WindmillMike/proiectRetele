import socket
from dnslib import DNSRecord, RR, QTYPE, A
import os

LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 53
BLOCKED_IP = "0.0.0.0"
FORWARD_DNS = "8.8.8.8" 

# Încarcă blacklist-ul
with open("/elocal/blacklist.txt") as f:
    blacklist = set(
        line.strip().split()[-1].lower()
        for line in f
        if line.strip() and not line.startswith("#")
    )

# Asigură-te că directorul există
log_path = "/elocal/loguri"
os.makedirs(log_path, exist_ok=True)

# Fișierul în care se vor salva domeniile blocate
blocked_log_file = os.path.join(log_path, "blocate.txt")

# Inițializează socket UDP pentru ascultare
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

print(f"DNS Server ascultă pe {LISTEN_IP}:{LISTEN_PORT}")

while True:
    try:
        data, addr = sock.recvfrom(512)
        request = DNSRecord.parse(data)
        qname = str(request.q.qname).rstrip('.').lower()

        print(f"Întrebare DNS: {qname} de la {addr}")

        if qname in blacklist:
            # Dacă e blocat → răspunde local cu 0.0.0.0
            reply = request.reply()
            reply.add_answer(RR(qname, QTYPE.A, rdata=A(BLOCKED_IP), ttl=60))
            print(f"Domeniu blocat — {qname} → {BLOCKED_IP}")

            # Salvează domeniul blocat în fișier
            with open(blocked_log_file, "a") as log:
                log.write(qname + "\n")

            sock.sendto(reply.pack(), addr)
        else:
            # Altfel → forward către un DNS real (Google)
            fwd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            fwd_sock.settimeout(2)
            fwd_sock.sendto(data, (FORWARD_DNS, 53))
            fwd_data, _ = fwd_sock.recvfrom(512)
            sock.sendto(fwd_data, addr)
            print(f"Domeniu permis — {qname} (forwardat către {FORWARD_DNS})")
    except Exception as e:
        print(f"Eroare: {e}")
