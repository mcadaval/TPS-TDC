from scapy.all import *
from config import BROADCAST_ADDRESS


class Package:
    def __init__(self, pkt):

        if pkt.payload:
            payload = pkt.payload
            protocol = payload.name

        if pkt.dst == BROADCAST_ADDRESS:
            destination_type = "BROADCAST"
        else:
            destination_type = "UNICAST"

        self.protocol = protocol
        self.destination_type = destination_type

    def protocol(self):
        return self.protocol
    
    def destination_type(self):
        return self.destination_type

    def symbol(self):
        return (self.destination_type, self.protocol)

    def __str__(self):
        return self.protocol