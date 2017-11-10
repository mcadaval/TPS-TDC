import math
from models.Hop import Hop

tau_table = [-1, -1, -1, 1.1511, 1.4250, 1.5712, 1.6563, 1.7110, 1.7491, 1.7770, 1.7984, 1.8153, 1.8290, 1.8403, 1.8498,
             1.8579, 1.8649, 1.8710, 1.8764, 1.8811, 1.8853, 1.8891, 1.8926, 1.8957, 1.8985, 1.9011, 1.9035, 1.9057,
             1.9078, 1.9096, 1.9114, 1.9130, 1.9146, 1.9160, 1.9174, 1.9186, 1.9198, 1.9209, 1.9220, -1, 1.9240]

# TODO borrar cuando ya no se use
numbers = [48.9, 49.2, 49.2, 49.3, 49.3, 49.8, 49.9, 50.1, 50.2, 50.5]


# TODO borrar cuando ya no se use
def create_hops(list):
    hops = []
    for value in list:
        params = {
            'rtt': value,
            'hop_numb': 1,
            'ip_address': "1",
            'intercontinental_jump': False
        }
        hops.append(Hop(params))
    return hops


# TODO borrar cuando ya no se use
def example():
    res = cimbala(create_hops(numbers))
    for hop in res:
        print(hop)


def cimbala(hops):
    hops.sort(key=lambda hop: hop.rtt, reverse=True)

    intercontinental_hops = []
    iterate = len(hops) > 1

    while iterate:

        rtt_mean = mean(hops)
        std_deviation = standard_deviation(hops, rtt_mean)

        first_element_z_rtt_value = z_rtt_value(hops[0].rtt, rtt_mean, std_deviation)
        last_element_z_rtt_value = z_rtt_value(hops[-1].rtt, rtt_mean, std_deviation)

        hop = {}

        if first_element_z_rtt_value > last_element_z_rtt_value:
            hop['hop_index'] = 0
            hop['zrtt_value'] = first_element_z_rtt_value
            is_max = True
        else:
            hop['zrtt_value'] = last_element_z_rtt_value
            hop['hop_index'] = -1
            is_max = False

        if is_outlier(hops, hop['zrtt_value']):
            if is_max:
                hops[hop['hop_index']].intercontinental_jump = True
            intercontinental_hops.append(hops[hop['hop_index']])
            del hops[hop['hop_index']]
        else:
            iterate = False

        iterate = iterate and len(hops) > 1

    hops = hops + intercontinental_hops
    hops.sort(key=lambda hop: hop.hop_numb, reverse=False)
    return hops


def is_outlier(hops, zrtt_value):
    res = False
    if zrtt_value > tau_table[(len(hops) - 1)]:
        res = True
    return res


def z_rtt_value(rtt, mean, std_deviation):
    return abs(rtt - mean) / std_deviation


def mean(list):
    sum_rtt = 0
    for hop in list:
        sum_rtt += hop.rtt

    return sum_rtt / len(list)


def standard_deviation(list, mean):
    acum = 0
    for hop in list:
        acum += pow((hop.rtt - mean), 2)

    return math.sqrt((1 / (len(list) - 1) * acum))


def calculate_z_rtt_values(hops):
    # saco respuestas vacias
    filtered_hops = [hop for hop in hops if hop.rtt != None]

    z_rtts = []
    # calculo media y desvio standard
    mean_hops = mean(filtered_hops)
    std_deviation = standard_deviation(filtered_hops, mean_hops)

    # calculo zrtt
    for hop in filtered_hops:
        z_rtt = z_rtt_value(hop.rtt, mean_hops, std_deviation)
        z_rtts.append(z_rtt)

    # agrego elementos nulos para que los puntoss se correspondan con su numero de salto en el grafico
    for i in range(0, len(hops)):
        if hops[i].rtt == None:
            z_rtts.insert(i, None)

    return z_rtts
