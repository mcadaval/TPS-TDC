from __future__ import print_function
from scapy.all import *
from model.Source import Source
from helpers import Parser
import sys


def process(rute):
    packets = rdpcap('../' + rute)
    symbols = Parser.parse(packets)
    source = Source(symbols)

    print('Cantidad total de paquetes: ', source.get_amount_of_symbols())
    print('Entriopia: ', source.get_entropy())
    print('Entriopia Maxima: ', source.get_max_entropy())
    print(source)

    for s in source.get_hosts():
        print(s)



if __name__ == '__main__':
    print('Usage: python3 main.py <rute to pcap>')
    if len(sys.argv) > 1:
        process(sys.argv[1])

    while True:
        rute = input("Ingrese la ruta del pcap, 'q' para salir: \n")
        if rute == 'q':
            exit(0)
        process(rute)
