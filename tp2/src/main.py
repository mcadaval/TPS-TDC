
from helpers.Traceroute import Traceroute
import sys
import helpers.Plotter as Plot

if __name__ == '__main__':
    dest = sys.argv[1]
    life_span = int(sys.argv[2])

    traceroute = Traceroute(dest, life_span)
    hops = traceroute.traceroute()
    Plot.rtt_between_jumps_graph(hops)
    Plot.build_map(hops)


