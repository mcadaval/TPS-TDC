from scapy.all import *
from config import BROADCAST_ADDRESS


class Package:
    def __init__(self, pkt):

        if IP in pkt or IPv6 in pkt:
            protocol = "IP"
            source = pkt['IP'].src
            destiny = pkt['IP'].dst

        elif ARP in pkt:
            protocol = "ARP"
            source = pkt['ARP'].psrc
            destiny = pkt['ARP'].pdst

        elif TCP in pkt:
            protocol = "TCP"
            source = pkt['TCP'].psrc
            destiny = pkt['TCP'].pdst

        elif UDP in pkt:
            protocol = "UDP"
            source = pkt['UDP'].psrc
            destiny = pkt['UDP'].pdst

        else:
            source = None
            destiny = None
            protocol = 'NONE'

        if source == BROADCAST_ADDRESS:
            destiny_type = "BROADCAST"
        else:
            destiny_type = "UNICAST"

        self.protocol = protocol
        self.source = source
        self.destiny = destiny
        self.destiny_type = destiny_type

    def __str__(self):
        return self.protocol
