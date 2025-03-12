#! /bin/sh
rm -f /logs/traffic.pcap
tcpdump -tttt -i eth0 icmp -c 10000 -w /logs/traffic.pcap
