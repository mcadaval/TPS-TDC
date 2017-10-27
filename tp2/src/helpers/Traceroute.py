from scapy.all import *
import helpers.Logger as logger
from datetime import datetime


class Traceroute:
    def __init__(self, dest, life_span):
        self.dest = dest
        self.life_span = life_span

    def create_packet(self, dest, ttl):
        packet = IP(dst=dest, ttl=ttl) / ICMP(type="echo-request")
        return packet

    def send_packet(self, packet, times):
        responses = []
        sum_of_times = 0
        valid_responses = 0

        for i in range(times):

            response = sr1(packet, timeout=2)

            if response != None:
                start = datetime.fromtimestamp(response.sent_time)
                end = datetime.fromtimestamp(response.time)
                delta = end - start
                sum_of_times += delta
                valid_responses += 1

            responses.append(response)

        if valid_responses == 0:
            valid_responses = 1

        average_time = sum_of_times / valid_responses

        result = {
            'average_time': average_time,
            'responses': responses
        }

        return result

    def traceroute(self):
        responses = []
        for ttl in range(self.life_span):
            packet = self.create_packet(self.dest, ttl)
            logger.print_iterarion(ttl)
            responses.append(self.send_packet(packet, 3))

        logger.print_responses(responses)
