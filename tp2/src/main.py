
from helpers.Traceroute import Traceroute
import sys
import helpers.Plotter as Plot
import helpers.Cimbala as cimbala

def printHelp():
    print("Cantidad inválida de argumentos")
    print("Modo de uso:")
    print("   python3", sys.argv[0], "<ip|url> <ttl_maximo>")
    print("Ejemplo:")
    print("   python3", sys.argv[0],"dc.uba.ar 20")
    exit(1)

if __name__ == '__main__':
        
    if len(sys.argv) != 3:
        printHelp();
        
    dest = sys.argv[1]
    life_span = int(sys.argv[2])

    traceroute = Traceroute(dest, life_span)
    hops = traceroute.traceroute()
    Plot.rtt_between_jumps_graph(hops)
    Plot.z_rtt_between_jumps_graph(hops, cimbala.calculate_z_rtt_values(hops))
    Plot.build_map(hops)


