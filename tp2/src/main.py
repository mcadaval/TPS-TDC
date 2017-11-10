from helpers.Traceroute import Traceroute
import sys
import helpers.Plotter as Plot
import helpers.Cimbala as cimbala


def printHelp():
    print("Cantidad inválida de argumentos")
    print("Modo de uso:")
    print("   python3", sys.argv[0], "<ip|url> [ttl_maximo] [debug_mode]")
    print("Ejemplos:")
    print("   python3", sys.argv[0], "dc.uba.ar 20 true")
    print("   python3", sys.argv[0], "dc.uba.ar 20")
    print("   python3", sys.argv[0], "dc.uba.ar")
    exit(1)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        printHelp()

    dest = sys.argv[1].replace("http://", '').replace("https://", '')
    life_span = 100
    debug = False

    if len(sys.argv) > 2:
        life_span = int(sys.argv[2])
        if len(sys.argv) > 3:
            debug = bool(sys.argv[3])

    traceroute = Traceroute(dest, life_span, debug)
    hops = traceroute.traceroute()

    if debug:
        Plot.rtt_between_jumps_graph(hops)
        Plot.z_rtt_between_jumps_graph(hops, cimbala.calculate_z_rtt_values(hops))
        Plot.build_map(hops)
