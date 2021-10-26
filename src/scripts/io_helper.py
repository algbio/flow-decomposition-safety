'''
io_helper reads and writes graphs to files
'''
import networkx as nx
import re

# ADAPTED FROM ARIEL/LUCY'S CODE
# source: https://github.com/lgw2/create_transcript_data/blob/master/input_and_truth_from_gtf.py

# ADAPTION OF ARIEL/LUCY'S CODE ENDS HERE
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
                    graphs.append(new_nx_graph([(x, nodes_to_add[x]) for x in nodes_to_add],
                                               edges_to_add))
                edges_to_add = []
                nodes_to_add = {}
            # Edge line in gfa file
            if line[0] == 'L':
                v_from = int(read[1])
                v_to = int(read[3])
                weight = int((read[5])[0:-1])
                edges_to_add.append(
                    (v_from, v_to, {'weight': weight, 'weight_copy': weight}))
                if v_from not in nodes_to_add:
                    nodes_to_add[v_from] = {'flow_in': 0, 'flow_out': 0}
                if v_to not in nodes_to_add:
                    nodes_to_add[v_to] = {'flow_in': 0, 'flow_out': 0}
                nodes_to_add[v_from]['flow_out'] += weight
                nodes_to_add[v_to]['flow_in'] += weight
    if edges_to_add:
        graphs.append(new_nx_graph([(x, nodes_to_add[x]) for x in nodes_to_add],
                                   edges_to_add))
    return graphs

def read_sg_file(filename):
    graphs = []
    with open(filename, 'r') as f:
        edges_to_add = []
        nodes_to_add = {}
        for i, line in enumerate(f):
            read = (line.rstrip()).split()
            # Title line in sg file, begins a new graph
            if line[0] == 'H':
                if i != 0 and len(edges_to_add)>0:
                    graphs.append(new_nx_graph([(x, nodes_to_add[x]) for x in nodes_to_add],
                                               edges_to_add))
                edges_to_add = []
                nodes_to_add = {}
            # Edge line in sg file
            if line[0] == 'L':
                v_from = read[1]
                v_to = read[3]
                weight = int((read[5]))
                edges_to_add.append(
                    (v_from, v_to, {'weight': weight, 'weight_copy': weight}))
                if v_from not in nodes_to_add:
                    nodes_to_add[v_from] = {'flow_in': 0, 'flow_out': 0}
                if v_to not in nodes_to_add:
                    nodes_to_add[v_to] = {'flow_in': 0, 'flow_out': 0}
                nodes_to_add[v_from]['flow_out'] += weight
                nodes_to_add[v_to]['flow_in'] += weight
    if edges_to_add:
        graphs.append(new_nx_graph([(x, nodes_to_add[x]) for x in nodes_to_add],
                                   edges_to_add))
    return graphs

def new_nx_graph(nodes, edges):
    '''
    new_nx_graph(nodes, edges) -> nx.DiGraph

    Creates new graph from given node and edge list and returns it.
    Assumes that souce of the graph is 0 and sink of the graph is number of nodes -1.
    '''
    #TODO: fix this such you don't have to always change this according to datatype
    #TODO: either change data to be in correct form or make some kind of guard for different type of extensions
    # use this for vertex based data
    graph = nx.DiGraph(edges, source='0', sink=f'{len(nodes)-1}')
    #this for sequence based data
    #graph = nx.DiGraph(edges, source='(0,0)', sink=f'(-1,-1)')
    graph.update(nodes=nodes)
    return graph


def read_file(filename, type=None):
    '''
    read_file(filename, type) -> list of graphs

    Reads given file and returns list of graphs as a list of paths.
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
                path = read_path(line, type)
                graph.append(path)
    graphs.append(graph)
    return graphs

def read_index_file(filename):
    indices = []
    flow_decompositions = []
    flow_dec = []
    temp = []
    with open(filename, 'r') as f:
        for line in f:
            # Hashtag(#) begins a graph defenition in file
            if line[0] == '#':
                if len(flow_dec) > 0:
                    flow_decompositions.append(flow_dec)
                    flow_dec = []
                    indices.append(temp)
                    temp = []
            # File line is a path
            else:
                if line[0] == '(':
                    res=re.findall(r'\((\d+,\d+)\)', line)
                    temp.append([(int(x.split(',')[0]),int(x.split(',')[1])) for x in res])
                else:
                    path = read_special_path(line)
                    flow_dec.append(path)
                
    flow_decompositions.append(flow_dec)
    indices.append(temp)
    return flow_decompositions, indices


def read_path(line, type=None):
    '''
    read_path(type, line) -> path as a tuple
    Reads path from given line. Path is constructed according to type 
    of the graph which determines how the paths are reported in file.
    Returns read path as a integer tuple where integers represent 
    vertices of the graph.
    TODO: change to use numpy vector?
    '''
    parts = line.rstrip().split()
    if type == 'catfish':
        return tuple([int(x) for x in parts[7:(len(parts))]])
    if type == 'truth':
        return tuple([int(x) for x in parts[1:(len(parts))]])
    return tuple([int(x) for x in parts[0:(len(parts))]])

def read_special_path(line):
    parts = line.rstrip().split()
    return tuple([int(x) for x in parts[0:(len(parts)-1)]])