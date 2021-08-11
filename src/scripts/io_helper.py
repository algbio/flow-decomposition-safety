'''
io_helper reads and writes graphs to files
'''
import networkx as nx

def read_gfa_file(filename):
    '''
    read_gfa_file(filename) -> nx.graph list
    Reads given file and return graphs described in .gfa file as a list of nx directed graphs.
    '''
    graphs = []
    with open(filename, 'r') as f:
        edges_to_add = []
        nodes_to_add = {}
        for i, line in enumerate(f):
            read = (line.rstrip()).split()
            # Title line in gfa file, begins a new graph
            if line[0] == 'H':
                if i != 0:
                    graphs.append(new_nx_graph([(x,nodes_to_add[x]) for x in nodes_to_add],
                     edges_to_add))
                edges_to_add = []
                nodes_to_add = {}
            # Edge line in gfa file
            if line[0] == 'L':
                v_from = int(read[1])
                v_to = int(read[3])
                weight = int((read[5])[0:-1])
                edges_to_add.append((v_from, v_to, {'weight':weight, 'weight_copy':weight}))
                if v_from not in nodes_to_add:
                    nodes_to_add[v_from] = {'flow_in':0, 'flow_out':0}
                if v_to not in nodes_to_add:
                    nodes_to_add[v_to] = {'flow_in':0, 'flow_out':0}
                nodes_to_add[v_from]['flow_out'] += weight
                nodes_to_add[v_to]['flow_in'] += weight
    if edges_to_add:
        graphs.append(new_nx_graph([(x,nodes_to_add[x]) for x in nodes_to_add],
                     edges_to_add))
    return graphs

def new_nx_graph(nodes, edges):
    '''
    new_nx_graph(nodes, edges) -> nx.DiGraph
    
    Creates new graph from given node and edge list and returns it.
    Assumes that souce of the graph is 0 and sink of the graph is number of nodes -1.
    TODO: Maybe change source/sink calculation if needed? In the catfish usecase this is not necessary.
    '''
    graph = nx.DiGraph(edges, source=0, sink=len(nodes)-1)
    graph.update(nodes = nodes)
    return graph

def read_file(filename, type):
    '''
    read_file(filename, type) -> list of graphs
    
    Reads given file and returns list of graphs as a list of paths.
    TODO: Make path a class?
    '''
    graphs = []
    graph = []
    with open(filename, 'r') as f:
        for line in f:
            # Hashtag(#) begins a graph defenition in file
            if line[0] == '#':
                if len(graph) > 0:
                    graphs.append(graph)
                    graph = []
            # File line is a path
            else:
                path = read_path(type, line)
                graph.append(path)
    graphs.append(graph)
    return graphs

def read_path(type, line):
    '''
    read_path(type, line) -> path as a tuple
    Reads path from given line. Path is constructed according to type 
    of the graph which determines how the paths are reported in file.
    Returns read path as a integer tuple where integers represent 
    vertices of the graph.
    TODO: change to use numpy vector?
    '''
    parts = line.rstrip().split()
    if type == 'safety':
        return tuple([int(x) for x in parts[0:(len(parts))]])
    if type == 'catfish':
        return tuple([int(x) for x in parts[7:(len(parts))]])
    if type == 'truth':
        return tuple([int(x) for x in parts[1:(len(parts))]])