from scapy.all import *
from datetime import datetime
import helpers.Logger as logger
import models.Hop as hop
import helpers.Cimbala as cimbala
import time



repeat_send_packet = 3

def create_hops(list):
    hops = []
    for value in list:
        params = {
            'rtt': value['rtt'],
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
        print("ttl "+str(ttl))
        result = None
        host_ip = None
        send_success = False

        minimum_time = 99999999999
        for i in range(times):

            packet = self.create_packet(self.dest, ttl)
            
            start = datetime.fromtimestamp(time.time())
            response = sr1(packet, timeout=2, verbose=False)
            end = datetime.fromtimestamp(time.time())
            delta = end - start
            response_time_ms = delta.total_seconds()*1000
            
            if response != None:
                if response[ICMP].type == 11:           # type 11 = 'time-exceeded'
                    print('time-exceeded')    
                else:
                    if response[ICMP].type == 0:
                        send_success = True


                #start = datetime.fromtimestamp(packet.time)
                #end = datetime.fromtimestamp(response.time)
                #delta = end - start
                #response_time_ms = delta.total_seconds()*1000
                if minimum_time > response_time_ms:
                    minimum_time = response_time_ms
                    host_ip = response.src


        result = {
            'rtt': minimum_time,        # rtt entre origen y destino al momento de finizar el ttl
            'ip_address': host_ip,
            'ttl': ttl
        }
        #print(result)

        return result, send_success

    def traceroute(self):
        responses = []
        for ttl in range(self.life_span):
            response, send_success = self.send_packet(repeat_send_packet, ttl)
            responses.append(response)
            if send_success:
                break

        # saco respuestas vacias
        responses = [hop for hop in responses if hop['ip_address'] != None]

        # saco duplicados
        filtered_responses = []
        for i in range(len(responses)):
            if i > 0:
                hop = responses[i]
                if hop['ip_address'] != responses[i-1]['ip_address']:
                    filtered_responses.append(responses[i])
                    break
            else:
                filtered_responses.append(responses[i])
                    

        
        # seteo el rtt como el tiempo de un salto
        for i in reversed(range(len(filtered_responses))):
            if i > 0:
                hop = filtered_responses[i]
                hop['rtt'] = hop['rtt'] - filtered_responses[i-1]['rtt']

        hops = create_hops(filtered_responses)

        hops = cimbala.cimbala(hops)

        for hop in hops:
            print(str(hop))

        




