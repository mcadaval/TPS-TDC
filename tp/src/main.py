from __future__ import print_function
from scapy.all import *

from model.Package import Package

packets = rdpcap('data/test.pcap')

list = []
for pkt in packets:
    package = Package(pkt)
    print(package)
    list.append(package)

