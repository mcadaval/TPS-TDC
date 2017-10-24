from models.Hop import Hop
import sys

hop = Hop({
    'rtt': "rtt",git
    'ip_address': "rtt",
    'intercontinental_jump': "rtt",
    'hop_numb': "rtt", })

print(hop.to_json())


'''
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
        
'''
