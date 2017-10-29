import json

class Hop:
    def __init__(self, params):
        self.rtt = params['rtt']
        self.ip_address = params['ip_address']
        self.intercontinental_jump = params['intercontinental_jump']
        self.hop_numb = params['hop_numb']
        

    def get_rtt(self):
        return self.rtt

    def get_ip_address(self):
        return self.ip_address

    def get_intercontinental_jump(self):
        return self.intercontinental_jump

    def get_hop_numb(self):
        return self.hop_numb

    def to_dicc(self):
        return {
            'rtt': self.rtt,
            'ip_address': self.ip_address,
            'intercontinental_jump': self.intercontinental_jump,
            'hop_numb': self.hop_numb
        }

    def to_json(self):
        return json.dumps(self.to_dicc())
