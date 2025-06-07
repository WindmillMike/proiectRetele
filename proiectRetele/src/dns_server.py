import socket
from dnslib import DNSRecord, RR, QTYPE, A

LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 8053
FAKE_IP = "1.2.3.4"
BLOCKED_IP = "0.0.0.0"

with open("../blacklist.txt") as f:
    blacklist = {
        line.split()[1].strip().lower()
        for line in f
        if line.strip() and not line.startswith("#") and len(line.split()) == 2
    }

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

print(f"DNS Server asculta pe {LISTEN_IP}:{LISTEN_PORT}")

while True:
    try:
        data, addr = sock.recvfrom(512)
        request = DNSRecord.parse(data)
        qname = str(request.q.qname).rstrip('.').lower()

        print(f"Intrebare DNS: {qname} de la {addr}")

        reply = request.reply()
        if qname in blacklist:
            reply.add_answer(RR(qname, QTYPE.A, rdata=A(BLOCKED_IP), ttl=60))
            print(f"Domeniu blocat — {qname} → {BLOCKED_IP}")
        else:
            reply.add_answer(RR(qname, QTYPE.A, rdata=A(FAKE_IP), ttl=60))
            print(f"Domeniu permis — {qname} → {FAKE_IP}")

        sock.sendto(reply.pack(), addr)
    except Exception as e:
        print(f"Eroare: {e}")
