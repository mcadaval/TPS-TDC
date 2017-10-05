import math


class Source:
    def __init__(self, symbols):
        self.symbols = symbols
        self.symbols_occurrences = None
        self.symbols_probabilities = None
        self.symbols_info = None
        self.average_info = None
        self.entropy = None

        self.get_symbols_ocurrences()
        self.get_symbols_probabilites()
        self.get_entropy()
        self.get_symbols_info()

    def get_amount_of_symbols(self):
        return len(self.symbols)

    def get_symbols_ocurrences(self):
        if not self.symbols_occurrences:
            symbols_occurrences = {}
            for symbol in self.symbols:
                if symbol in symbols_occurrences:
                    symbols_occurrences[symbol] += 1
                else:
                    symbols_occurrences[symbol] = 1
            self.symbols_occurrences = symbols_occurrences

        return self.symbols_occurrences

    def get_symbols_probabilites(self):
        if not self.symbols_probabilities:
            symbols_probabilities = {}
            total_symbols = len(self.symbols)
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
        tuples = [(key, value) for key, value in self.get_symbols_info()]

        tuples = filter(lambda element: element[1] < self.average_info * 0.8, tuples)
        return tuples

    def get_symbols_info(self):
        if not self.symbols_info:
            symbols_info = {}
            total_info = 0
            for symb, occurrences in self.get_symbols_ocurrences().items():
                info = math.log2(self.get_amount_of_symbols() / occurrences)
                symbols_info[symb] = info
                total_info = total_info + info
            self.average_info = total_info / self.get_amount_of_symbols()
            self.symbols_info = symbols_info

        return self.symbols_info

    def __str__(self):
        res = ''
        for symb, occurrences in self.symbols_occurrences.items():
            res += 'symbol: ' + str(symb) + ' occurrences: ' + str(occurrences) + ' probability:' + str(
                self.symbols_probabilities[
                    symb]) + '\n'

        return res
