from __future__ import print_function
from scapy.all import *
from model.Source import Source
from helpers import Parser
from helpers import GraphHelper
import sys

BAR_CHART_PROTOCOLS = True
HOST_GRAPH = False
SIMPLE_HOST_GRAPH = False
BAR_CHART_INFO_S1 = True
BAR_CHART_INFO_S2 = True

def process(rute):
    packets = rdpcap(rute)
    source_protocols = Source(Parser.parseS1(packets))
    source_hosts = Source(Parser.parseS2(packets))

    print('Cantidad total de simbolos(S1): ', source_protocols.get_capture_size())
    print('Entropia(S1): ', source_protocols.get_entropy())
    print('Entropia Maxima(S1): ', source_protocols.get_max_entropy())
    print('Cantidad de simbolos distintos(S1): ', source_protocols.get_number_of_symbols())
    print('Porcentaje de paquetes broadcast(S1): ', source_protocols.calculate_broadcast_percentage())
    print('\n')
    print('Cantidad total de simbolos(S2): ', source_hosts.get_capture_size())
    print('Entropia(S2): ', source_hosts.get_entropy())
    print('Entropia Maxima(S2): ', source_hosts.get_max_entropy())
    print('Cantidad de simbolos distintos(S2): ', source_hosts.get_number_of_symbols())
    print('Informacion promedio(S2): ', source_hosts.get_average_info())
    print('Cota de informacion para distinguir simbolos(S2): ', source_hosts.get_average_info() * 0.8)
    
    print('\n')    
    print('Simbolos(S1): ')
    source_protocols.print_symbols()
    print('\n')    
    print('Simbolos distinguidos(S2): ')
    source_hosts.print_distinguished_symbols()


    if BAR_CHART_INFO_S1:
        GraphHelper.info_entropy_maxentropy(source_protocols.get_symbols_info(), source_protocols.get_entropy(), source_protocols.get_max_entropy())
    
    if BAR_CHART_INFO_S2:
        GraphHelper.info_entropy_maxentropy(source_hosts.get_distinguished_symbols_info(), source_hosts.get_entropy(), source_hosts.get_max_entropy())

    if BAR_CHART_PROTOCOLS:
        GraphHelper.protocols_percentage(source_protocols.calculate_protocols_probabilites())

    if HOST_GRAPH:
        hostsGraph = GraphHelper.createGraph(packets)
        GraphHelper.drawGraph(hostsGraph, False, False)

    if SIMPLE_HOST_GRAPH:
        hostsGraph = GraphHelper.createGraph(packets)
        simplerHostsGraph = GraphHelper.unionSimilarNodes(hostsGraph)    
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
    