from model.Package import Package


def parse(packets):
    symbols = []
    for pkt in packets:
        packet = Package(pkt)
        symbols.append(packet.symbol())

    return symbols



def parseSrc(packets):
    symbols = []
    for pkt in packets:
        if 'ARP' in pkt:
            symbols.append(pkt['ARP'].pdst)
    return symbols
