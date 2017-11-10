from scapy.all import *
from datetime import datetime
import helpers.Logger as logger
import models.Hop as hop
import helpers.Cimbala as cimbala
import time

repeat_send_packet = 20  # cantidad de paquetes ICMP por TTL
use_average = False  # True para calcular rtt como promedio, False para calcular rtt como minimo
timeout = 1  # timeout en segundos para la respuesta ICMP esperada


def create_hops(list):
    hops = []
    for value in list:
        params = {
            'rtt': round(value['rtt'], 4),
            'hop_numb': value['ttl'],
            'ip_address': value['ip_address'],
            'intercontinental_jump': False
        }
        hops.append(hop.Hop(params))
    return hops


class Traceroute:
    def __init__(self, dest, life_span):
        self.dest = dest
        self.life_span = life_span

    def create_packet(self, dest, ttl):
        packet = IP(dst=dest, ttl=ttl) / ICMP(type="echo-request")
        return packet

    def send_packet(self, times, ttl):
        print("ttl " + str(ttl))
        host_ip_minimum = None
        host_ip_average = None
        send_success = False

        minimum_time = 99999999999
        sum_of_times = 0
        for i in range(times):
            # creo paquete ICMP echo-request, lo envio y mido el rtt 
            packet = self.create_packet(self.dest, ttl)
            start = datetime.fromtimestamp(time.time())
            response = sr1(packet, timeout=timeout, verbose=False)
            end = datetime.fromtimestamp(time.time())
            delta = end - start
            response_time_ms = delta.total_seconds() * 1000

            # verifico tipo de respuesta, si es que la hay
            if response != None:
                if response[ICMP].type == 11:  # type 11 = 'time-exceeded'
                    print(i, ' time-exceeded')
                else:
                    if response[ICMP].type == 0:  # type 0 = 'echo-reply'
                        send_success = True

                # start = datetime.fromtimestamp(packet.time)
                # end = datetime.fromtimestamp(response.time)
                # delta = end - start
                # response_time_ms = delta.total_seconds()*1000

                # verifico si el ultimo tiempo medidio es minimo
                if minimum_time > response_time_ms:
                    minimum_time = response_time_ms
                    host_ip_minimum = response.src

                # sumo el tiempo medido para luego calcular promedio
                sum_of_times += response_time_ms
                if host_ip_average == None:
                    host_ip_average = response.src

        # calculo promedio
        average_time = sum_of_times / times

        # dependiendo del valor de use_average uso promedio o minimo
        if use_average:
            rtt = average_time
            host_ip = host_ip_average
        else:
            rtt = minimum_time
            host_ip = host_ip_minimum

        result = {
            'rtt': rtt,  # rtt entre origen y destino para el ttl actual
            'ip_address': host_ip,
            'ttl': ttl
        }

        return result, send_success

    def add_null_hops(self, hops):
        i = 0
        max_hop = hops[-1].hop_numb
        while len(hops) < max_hop - 1:
            if hops[i].hop_numb + 1 < hops[i + 1].hop_numb:
                params = {
                    'rtt': None,
                    'hop_numb': hops[i].hop_numb + 1,
                    'ip_address': None,
                    'intercontinental_jump': None
                }
                hops.insert(i + 1, hop.Hop(params))
            i += 1
        return hops

    def traceroute(self):
        responses = []
        # envio rafagas de paquetes ICMP con distintos TTL 
        for ttl in range(self.life_span):
            response, send_success = self.send_packet(repeat_send_packet, ttl)
            responses.append(response)
            # si respondio la ip destino, dejamos de enviar paquetes
            if send_success:
                break

        # saco respuestas vacias
        responses = [hop for hop in responses if hop['ip_address'] != None]

        # saco duplicados
        filtered_responses = [responses[0]]
        for i in range(len(responses)):
            if i > 0:
                hop = responses[i]
                if hop['ip_address'] != filtered_responses[len(filtered_responses) - 1]['ip_address']:
                    filtered_responses.append(responses[i])

        # seteo el rtt como el tiempo de un salto
        for i in reversed(range(len(filtered_responses))):
            if i > 0:
                hop = filtered_responses[i]
                hop['rtt'] = hop['rtt'] - filtered_responses[i - 1]['rtt']

        # creo lista de hops a partir de las respuestas
        hops = create_hops(filtered_responses)

        # para aplicar cimbala quito primer hop 
        first_hop = hops[0]
        hops.pop(0)

        # aplico cimbala para verificar saltos intercontinentales
        hops = cimbala.cimbala(hops)
        # agrego el primer hop que saque antes        
        hops.insert(0, first_hop)

        # agrego null hops
        hops = self.add_null_hops(hops)

        print('[')
        for i in range(len(hops)):
            if i != len(hops)-1:
                print(hops[i].to_json()+',')
            else:
                print(hops[i].to_json())
        print(']')

        return hops
