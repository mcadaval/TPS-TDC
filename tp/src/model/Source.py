import math


class Source:
    def __init__(self, symbols):
        self.symbols_capture = symbols
        self.symbols = None        
        self.symbols_occurrences = None
        self.symbols_probabilities = None
        self.symbols_info = None
        self.average_info = None
        self.entropy = None

        self.get_symbols()
        self.get_symbols_ocurrences()
        self.get_symbols_probabilites()
        self.get_entropy()
        self.get_symbols_info()

    def get_symbols(self):
        if not self.symbols:
            symbols = []
            for symbol in self.symbols_capture:
                if symbol not in symbols:
                    symbols.append(symbol)
            
            self.symbols = symbols

        return self.symbols 

    def get_capture_size(self):
        return len(self.symbols_capture)
    
    def get_number_of_symbols(self):
        return len(self.symbols)

    def get_symbols_ocurrences(self):
        if not self.symbols_occurrences:
            symbols_occurrences = {}
            for symbol in self.symbols_capture:
                if symbol in symbols_occurrences:
                    symbols_occurrences[symbol] += 1
                else:
                    symbols_occurrences[symbol] = 1
            self.symbols_occurrences = symbols_occurrences

        return self.symbols_occurrences

    def get_symbols_probabilites(self):
        if not self.symbols_probabilities:
            symbols_probabilities = {}
            total_symbols = self.get_capture_size()
            for symb, occurrences in self.symbols_occurrences.items():
                symbols_probabilities[symb] = occurrences / total_symbols
            self.symbols_probabilities = symbols_probabilities

        return self.symbols_probabilities

    def get_entropy(self):
        if not self.entropy:
            entropy = 0
            for symb, probability in self.symbols_probabilities.items():
                entropy = entropy + probability * math.log2(1 / probability)
            self.entropy = entropy

        return self.entropy

    def get_max_entropy(self):
        return math.log2(len(self.symbols_probabilities))

    def get_hosts(self):
        tuples = [(symbol, info) for symbol, info in self.get_symbols_info().items()]
        print('average_info: '+str(self.average_info))
        tuples = list(filter(lambda element: element[1] < (self.average_info * 0.8), tuples))
        return tuples

    def get_symbols_info(self):
        if not self.symbols_info:
            symbols_info = {}
            total_info = 0
            for symb, probability in self.get_symbols_probabilites().items():            
                info = math.log2(1 / probability)                
                symbols_info[symb] = info
                total_info = total_info + info
            self.average_info = total_info / self.get_number_of_symbols()
            self.symbols_info = symbols_info

        return self.symbols_info

    def calculate_broadcast_percentage(self):
        amount_broadcast = 0
        for pkt in self.symbols:
            if pkt[0] == "BROADCAST":
                amount_broadcast = amount_broadcast + 1
        return amount_broadcast/len(self.symbols)*100

    def calculate_protocols_probabilites(self):
        protocols_percentage = {}

        for symbol in self.symbols:
            if symbol[1] in protocols_percentage:
                protocols_percentage[symbol[1]] += 1
            else:
                protocols_percentage[symbol[1]] = 1

        for protocol in protocols_percentage:
            protocols_percentage[protocol] = protocols_percentage[protocol]/len(self.symbols)

        return protocols_percentage

    def __str__(self):
        res = ''
        for symb, occurrences in self.symbols_occurrences.items():
            res += 'symb: ' + str(symb) + ' count: ' + str(occurrences) + ' prob: ' + str(
                self.symbols_probabilities[
                    symb])[0:7] + '\n'

        return res
