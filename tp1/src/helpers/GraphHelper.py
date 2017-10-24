import matplotlib.pyplot as plt
import networkx as nx
from model.Package import Package


def createGraph(packets):
    networkGraph = nx.DiGraph()
    for pkt in packets:
        if 'ARP' in pkt:
            src = pkt['ARP'].psrc
            dst = pkt['ARP'].pdst
            if src not in networkGraph.nodes():
                networkGraph.add_node(src, size=1)
            if dst not in networkGraph.nodes():
                networkGraph.add_node(dst, size=1)
            networkGraph.add_edge(pkt['ARP'].psrc, pkt['ARP'].pdst, weight = 1)
    #return nx.convert_node_labels_to_integers(networkGraph)
    return networkGraph


def drawGraph(graph, withNodeLabels):
    '''
    pos = nx.spring_layout(graph)
    
    nx.draw(graph, pos, node_shape = '.', with_labels = withNodeLabels)

    if withEdgeLabels:
        labels = nx.get_edge_attributes(graph,'weight')
        nx.draw_networkx_edge_labels(graph,pos,edge_labels=labels)

    plt.show()
    '''

    pos = nx.spring_layout(graph, k=0.3,iterations=10)
    #pos = nx.shell_layout(graph)
    #pos = nx.random_layout(graph)
    for n in graph.nodes():
        l = []
        l.append(n)
        nodeSize = graph.node[n]['size']
        nodeColor = 'g'
        labels = {}
        labels[n] = nodeSize
        nx.draw_networkx(graph, pos, nodelist=l, labels= labels, node_size = 400+nodeSize*150, node_color=nodeColor ,node_shape = '.', with_labels = withNodeLabels, width=0.5)
    plt.axis('off')
    plt.show()
    


# Junta varios nodos en uno solo si es que todos son solamente adyacentes de un mismo nodo
def unionSimilarNodes(graph):
    networkGraph = nx.DiGraph(graph)

    index = 0
    for node in graph.nodes():
        neighbors = graph.successors(node)
        sameNodes = 0
        for neighbor in neighbors:
            if len(list(graph.predecessors(neighbor))) == 1 and len(list(graph.successors(neighbor))) == 0:
                networkGraph.remove_node(neighbor)
                sameNodes = sameNodes + 1
        if sameNodes > 0:
            networkGraph.add_node(index, size=sameNodes)
            networkGraph.add_edge(node, index, weight=sameNodes)
            index = index + 1
    return networkGraph



def barChar(labels_map, showLegend, threshold = 0):
    fig, ax = plt.subplots()
    index = 0
    for label, value in labels_map.items():
        print(label, value)
        ax.bar(index*2, value, label=label)
        index = index+1
    
    if threshold > 0:
        ax.plot([0., 35], [threshold, threshold], "k--")

    if showLegend:
        plt.legend()
    plt.show()
    
