#!/bin/bash
set -x

# Configurare rutare
ip route del default
ip route add default via 198.7.0.1

# DNS extern fallback
echo "nameserver 8.8.8.8" >> /etc/resolv.conf

# Previne închiderea TCP-urilor hand-made
iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP

# Pornește DNS serverul
python3 /elocal/src/dns_server.py
