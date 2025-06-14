#!/bin/bash
set -x

until ping -c1 198.7.0.1 &> /dev/null; do
    echo "[middle.sh] Aștept routerul să devină disponibil..." #Pentru ca nu gaseste ruta de ip a clientului
    sleep 1
done

ip route add 172.7.0.0/16 via 198.7.0.1

echo "nameserver 8.8.8.8" >> /etc/resolv.conf

iptables -A OUTPUT -p tcp --tcp-flags

python3 /elocal/src/arp_spoof.py &