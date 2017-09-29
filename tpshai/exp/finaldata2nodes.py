from sys import argv
from ast import literal_eval

with open(argv[1]) as f:
    content = f.readlines()

last_line = content[-1]

start_of_list_idx = last_line.index('[')
end_of_list_idx = last_line.index(']')

list_string = last_line[start_of_list_idx:end_of_list_idx+1]

s1_network = literal_eval(list_string)

s1_network_total_nodes = set([dst for ((src, dst), info) in s1_network] + [src for ((src, dst), info) in s1_network])
s1_network_dsts = set([dst for ((src, dst), info) in s1_network])

print('Cantidad de IPs de origen distintas: ' + str(len(s1_network_total_nodes)))
print('Cantidad de IPs de destino (símbolos) distintas: ' + str(len(s1_network_dsts)))
print('IPs de destino (símbolos): ' + str(s1_network_dsts))
