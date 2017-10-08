from __future__ import print_function
from scapy.all import *
from model.Source import Source
from helpers import Parser
from helpers import GraphHelper
from matplotlib.pyplot import pause
import sys
import pylab

import random

pylab.ion()


hostsGraph = nx.DiGraph()
pylab.show()


def arp_display(pkt):
    print('arp sent: '+ str(pkt[ARP].psrc) + ' - ' + str(pkt[ARP].pdst))

    src = pkt[ARP].psrc
    dst = pkt[ARP].pdst
    if src not in hostsGraph.nodes():
        hostsGraph.add_node(src)
    if dst not in hostsGraph.nodes():
        hostsGraph.add_node(dst)
    hostsGraph.add_edge(pkt[ARP].psrc, pkt[ARP].pdst)
    nx.draw(hostsGraph, with_labels = True)
    pylab.draw()
    pause(1)
    


if __name__ == '__main__':
    sniff(prn=arp_display, filter="arp", store=0, count=0)


