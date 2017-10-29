import math

tau_table = [-1, -1, -1, 1.1511, 1.4250, 1.5712, 1.6563, 1.7110, 1.7491, 1.7770, 1.7984, 1.8153, 1.8290, 1.8403, 1.8498,
             1.8579, 1.8649, 1.8710, 1.8764, 1.8811, 1.8853, 1.8891, 1.8926, 1.8957, 1.8985, 1.9011, 1.9035, 1.9057,
             1.9078, 1.9096, 1.9114, 1.9130, 1.9146, 1.9160, 1.9174, 1.9186, 1.9198, 1.9209, 1.9220, -1, 1.9240]


def cimbala(hops):
    hops.sort(key=lambda hop: hop.rtt, reverse=True)
    intercontinental_hops = []

    while last_hop_is_intercontinental_jump(hops):
        intercontinental_hop = hops[-1]
        intercontinental_hop.intercontinental_jump = True
        intercontinental_hops = intercontinental_hops + intercontinental_hop
        hops = hops[0:len(hops) - 1]

    hops + intercontinental_hops
    hops.sort(key=lambda hop: hop.hop_numb, reverse=True)

    return hops


def last_hop_is_intercontinental_jump(hops):
    is_intercontinental_jump = False

    rtt_mean = mean(hops)
    last_element = hops[-1]
    z_rrt_value = z_rtt_value(last_element, rtt_mean, hops)
    if z_rrt_value > tau_table(len(hops) - 1):
        is_intercontinental_jump = True
    return is_intercontinental_jump


def z_rtt_value(hop, rtt_mean, hops):
    return (hop.rtt - rtt_mean) / (standar_deviation(hops, rtt_mean))


def mean(list):
    sum_rtt = 0
    for hop in list:
        sum_rtt += hop.rtt

    return sum_rtt / len(list)


def tau_table(index):
    tau_table[index]


def standar_deviation(list, mean):
    acum = 0
    for hop in list:
        acum = pow((hop.rtt - mean), 2)

    return math.sqrt((1 / len(list) * acum))
