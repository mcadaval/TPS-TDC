from __future__ import print_function
from scapy.all import *

from model.Package import Package

packets = rdpcap('../data/DatosEXACTAS-UBA.pcap')
# packets = rdpcap('../data/DatosLaboratorios-DC.pcap')

symbols_occurrences = {}
total_packets = 0

for pkt in packets:
    packet = Package(pkt)
    symbol = packet.symbol()
    if symbol in symbols_occurrences:
        symbols_occurrences[symbol] += 1
    else:
        symbols_occurrences[symbol] = 1    
    total_packets += 1

symbols_probabilities = {}
for symb, occurrences in symbols_occurrences.items():
    symbols_probabilities[symb] = occurrences/total_packets

print('Cantidad total de paquetes: ', total_packets)

for symb, occurrences in symbols_occurrences.items():
    print('symbol: ', symb)
    print('occurrences: ', occurrences)

for symb, probability in symbols_probabilities.items():
    print('symbol: ', symb)
    print('probability: ', probability)
