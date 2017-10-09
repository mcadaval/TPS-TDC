from __future__ import print_function
from scapy.all import *
from model.Source import Source
from helpers import Parser
from helpers import GraphHelper
import sys


def process(rute):
    packets = rdpcap(rute)
    symbols_capture = Parser.parse(packets)
    source_protocols = Source(symbols_capture)

    source_hosts = Source(Parser.parseSrc(packets))


    print('Cantidad total de paquetes: ', len(symbols_capture))
    print('Entropia: ', source_protocols.get_entropy())
    print('Entropia Maxima: ', source_protocols.get_max_entropy())
    print(source_protocols)

    print('Entropia hosts: ', source_hosts.get_entropy())
    print('Hosts identificados: ')
    for s in source_hosts.get_hosts():
        print(s)

    print('Porcentaje de paquetes broadcast', source_protocols.calculate_broadcast_percentage())

    print('Probabilidades de protocolos', source_protocols.calculate_protocols_probabilites())

    hostsGraph = GraphHelper.createGraph(packets)
    simplerHostsGraph = GraphHelper.unionSimilarNodes(hostsGraph)
    #GraphHelper.drawGraph(hostsGraph, False, False)
    GraphHelper.drawGraph(simplerHostsGraph, True)


if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        process(sys.argv[1])
    else:
        print('Usage: python3 main.py <rute to pcap>')

    while True:
        rute = input("Ingrese la ruta del pcap, 'q' para salir: \n")
        if rute == 'q':
            exit(0)
        process(rute)
    