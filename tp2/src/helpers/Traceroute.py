from scapy.all import *
from datetime import datetime
import helpers.Logger as logger
import models.Hop as hop
import time



class Traceroute:
    def __init__(self, dest, life_span):
        self.dest = dest
        self.life_span = life_span

    def create_packet(self, dest, ttl):
        packet = IP(dst=dest, ttl=ttl) / ICMP(type="echo-request")
        return packet

    def send_packet(self, times, ttl):
        print("ttl "+str(ttl))
        result = []
        hosts_ip = []
        send_success = False

        minimum_time = 999999999
        for i in range(times):

            packet = self.create_packet(self.dest, ttl)
            
            start = datetime.fromtimestamp(time.time())
            response = sr1(packet, timeout=2, verbose=False)
            end = datetime.fromtimestamp(time.time())
            delta = end - start
            #response_time_ms = delta.total_seconds()*1000
            
            if response != None:
                if response[ICMP].type == 11:           # type 11 = 'time-exceeded'
                    print('time-exceeded')    
                else:
                    print('type: '+str(response[ICMP].type))        # type 0 = 'echo-reply'
                    if response[ICMP].type == 0:
                        send_success = True

                if not response.src in hosts_ip:
                    hosts_ip.append(response.src)

                #start = datetime.fromtimestamp(packet.time)
                #end = datetime.fromtimestamp(response.time)
                #delta = end - start
                response_time_ms = delta.total_seconds()*1000
                if minimum_time > response_time_ms:
                    minimum_time = response_time_ms
                    hosts_ip = [response.src]


        for ip in hosts_ip:
            response = {
                'rtt': minimum_time,        # rtt entre origen y destino al momento de finizar el ttl
                'ip_address': ip,
                'ttl': ttl
            }
            result.append(response)
    

        return result, send_success

    def traceroute(self):
        responses = []
        for ttl in range(self.life_span):
            #logger.print_iterarion(ttl)
            response, send_success = self.send_packet(20, ttl)
            responses.append(response)
            if send_success:
                break

        # saco respuestas vacias
        responses = [hops for hops in responses if len(hops) > 0 and len([1 for hop in hops if hop['rtt'] > 0]) > 0]

        # saco duplicados
        filtered_responses = []
        for i in range(len(responses)):
            if i > 0:
                for hop in responses[i]:
                    if not hop['ip_address'] in [x['ip_address'] for x in responses[i-1]]:
                        filtered_responses.append(responses[i])
                        break
            else:
                filtered_responses.append(responses[i])
                    

        
        # seteo el rtt como el tiempo de un salto
        for i in reversed(range(len(filtered_responses))):
            if i > 0:
                for hop in filtered_responses[i]:
                    hop['rtt'] = hop['rtt'] - filtered_responses[i-1][0]['rtt']

        
        for e in filtered_responses:
            for hop in e:
                print(str(hop))

        #logger.print_responses(responses)
