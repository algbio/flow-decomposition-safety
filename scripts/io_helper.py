from graph import Graph
import networkx as nx

def write_file(str, output):
    f = open(output, 'a')
    f.write(f'{str} \n')

def read_gfa_file(filename):
    graphs = []
    graph = None
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            # read line
            read = (line.rstrip()).split('\t')
            # add edge
            if line[0] == 'H':
                if i != 0:
                    graphs.append(Graph(graph, 0, len(graph.nodes)-1))
                graph = nx.DiGraph()
            if line[0] == 'L':
                v_from = int(read[1])
                v_to = int(read[3])
                weight = int((read[5])[0:-1])
                graph.add_edge(v_from, v_to, capacity=weight)
                init_node(graph.nodes, v_from, v_to, weight)
    if graph is not None:
        graphs.append(Graph(graph, 0, len(graph.nodes)-1))
    return graphs

def init_node(nodes, v_from, v_to, weight):
    if 'flow_out' not in nodes[v_from]:
        nodes[v_from]['flow_out'] = 0
    if 'flow_out' not in nodes[v_to]:
        nodes[v_to]['flow_out'] = 0
    if 'flow_in' not in nodes[v_from]:
        nodes[v_from]['flow_in'] = 0
    if 'flow_in' not in nodes[v_to]:
        nodes[v_to]['flow_in'] = 0
    nodes[v_to]['flow_in'] += weight
    nodes[v_from]['flow_out'] += weight