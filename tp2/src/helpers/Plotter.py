import matplotlib.pyplot as plt

example = [{'rtt': 1}, {'rtt': 2}]


def rtt_graph(hops):
    x = range(0, len(hops))
    y = [hop['rtt'] for hop in hops]

    plt.plot(x, y, '-o')
    plt.show()
