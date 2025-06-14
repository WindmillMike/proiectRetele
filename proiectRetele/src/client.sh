#!/bin/bash
set -x
# remove default gateway 172.7.1.1
ip route del default

# make router container the default router
ip route add default via 172.7.0.1

# adaugă rută explicită către server
ip route add 198.7.0.2 via 172.7.0.1

# add DNS (serverul)
echo "nameserver 198.7.0.2" >> /etc/resolv.conf

# drop kernel TCP reset pentru conexiuni custom
iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP
