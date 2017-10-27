
from helpers.Traceroute import Traceroute
import sys

if __name__ == '__main__':
    dest = sys.argv[1]
    life_span = int(sys.argv[2])

    traceroute = Traceroute(dest, life_span)
    traceroute.traceroute()

