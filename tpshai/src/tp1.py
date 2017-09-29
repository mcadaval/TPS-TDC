# Usage: sudo python tp1.py <maximum_time_in_minutes> <interface_name> (optional: <experiment_name>)

from scapy.all import *
import math
import atexit
import sys
import time

BROADCAST_ADDRESS = 'ff:ff:ff:ff:ff:ff'
BROADCAST_SYMBOL = 'S_broadcast'
UNICAST_SYMBOL = 'S_unicast'
WHO_HAS_OP_CODE = 1

class Source(object):
    def __init__(self):
        self.freq = {}
        self.count = 0

    def relative_freq(self, s):
        return float(self.freq[s])/float(self.count)

    def new_occurrence(self, s):
        if s not in self.freq:
            self.freq[s] = 1
        else:
            self.freq[s] = self.freq[s] + 1
        self.count = self.count + 1

    def probability(self, s):
        return self.relative_freq(s)

    def information(self, s):
        return math.log(1/self.probability(s), 2)

    def symbols(self):
        return self.freq.keys()

    def entropy(self):
        res = 0
        for s in self.symbols():
            res = res + self.probability(s) * self.information(s)
        return res

    def freq2csv(self, file):
        freq_file = open(file, 'w')
        freq_file.write('symbol,freq\n')
        for k, v in self.freq.items():
            freq_file.write(res + str(k) + ',' + str(v) + '\n')
        freq_file.close()

    def information2csv(self, file):
        information_file = open(file, 'w')
        information_file.write('symbol,information\n')
        for k, v in self.freq.items():
            information_file.write(str(k) + ',' + str(self.information(k)) + '\n')
        information_file.close()

    def distinguished_nodes(self):
        res = []
        for s in self.symbols():
            if self.information(s) < self.entropy():
                res.append(s)
        return res

    def __repr__(self):
        return str([(s,self.probability(s)) for s in self.symbols()]) + ' | H = ' + str(self.entropy()) + ' | n = ' + str(self.count)

maximum_time = float(sys.argv[1]) * 60
start_time = float(time.time());
print('Sniffed seconds: ' + str(maximum_time))

interface_name = sys.argv[2]
    
S = Source()
S1 = Source()
S_network = Source()
S1_network = Source()

def print_final_data(file):
    final_data_file = open(file, 'w')
    final_data_file.write('S: ' + str(S) + '\n')
    final_data_file.write('S1: ' + str(S1) + '\n')
    final_data_file.write('S1\'s distinguished nodes: ' + str(S1.distinguished_nodes()) + '\n')
    final_data_file.write('S\'s network: ' + str(S_network) + '\n')
    final_data_file.write('S1\'s network: ' + str(S1_network))
    final_data_file.close()

def print_network(source, file):
    graph_file = open(file, 'w')
    graph_file.write('digraph G {\n')
    graph_file.write('    dpi="1000";\n')
    graph_file.write('    size="1,1";\n')
    for key, value in source.freq.items():
        graph_file.write('    ' + key[0] + ' -> ' + key[1] + ' [ label="' + str(value) + '" ];\n')
    graph_file.write('}')
    graph_file.close()

def atexit_function():
    print_final_data(sys.argv[3] + '-final-data.txt')
    if len(sys.argv) > 3:
        S.information2csv(sys.argv[3] + '-information-S.csv')
        S1.information2csv(sys.argv[3] + '-information-S1.csv')
        print_network(S_network, sys.argv[3] + '-graph-S.dot')
        print_network(S1_network, sys.argv[3] + '-graph-S1.dot')

def callback_S(pkt):
    dst = pkt.dst
    sys.stderr.write('All | ' + str(pkt.src) + ' --> ' + str(dst) + '\n')
    if str(dst) == BROADCAST_ADDRESS:
        S.new_occurrence(BROADCAST_SYMBOL)
    else:
        S.new_occurrence(UNICAST_SYMBOL)
    S_network.new_occurrence(('"' + str(pkt.src) + '"', '"' + str(dst) + '"'))

def callback_S1(pkt):
    if pkt.haslayer(ARP) and pkt.getlayer(ARP).op == WHO_HAS_OP_CODE:
        sys.stderr.write('ARP | ' + str(pkt[Ether].src) + ' --> ' + str(pkt[Ether].dst) + ' | ' + str(pkt[ARP].psrc) + ' --> ' + str(pkt[ARP].pdst) + '\n')
        S1.new_occurrence(str(pkt.getlayer(ARP).pdst))
        S1_network.new_occurrence(('"' + str(pkt.getlayer(ARP).psrc) + '"', '"' + str(pkt.getlayer(ARP).pdst) + '"'))

def callback(pkt):
    if float(time.time()) - start_time > maximum_time:
        sys.exit(0)
    callback_S(pkt)
    callback_S1(pkt)

def run_tp(iface):
    atexit.register(atexit_function)
    sniff(prn=callback, store=0, iface=iface)

if __name__ == '__main__':
    try:
        run_tp(interface_name)
    except IndexError as e:
        print('Usage: sudo python tp1.py <maximum_time_in_minutes> <interface_name> (optional: <experiment_name>)')