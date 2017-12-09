from model.Package import Package


def parseS1(packets):
    symbols = []
    for pkt in packets:
        packet = Package(pkt)
        symbols.append(packet.symbol())

    return symbols

def parseS2(packets):
    symbols = []
    for pkt in packets:
        if 'ARP' in pkt:
            symbols.append(pkt['ARP'].pdst)
    return symbols