'''
io_helper reads and graphs to files
'''
import networkx as nx


def write_file(str, output):
    '''
    write_file(str, output)
    Writes given string end of the given output file.
    '''
    f = open(output, 'a')
    f.write(f'{str}')


def read_gfa_file(filename):
    '''
    read_gfa_file(filename) -> list of nx.graph
    Reads given file and return graphs described in .gfa file as a list of nx directede graphs.
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
                edges_to_add.append((v_from, v_to, {'weight':weight}))
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

# fix this to not to be dependent on path of the file
def read_file(filename, type=None):
    
    filename_parts = filename.split('/')

    graphs = []
    graph = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.rstrip().split(' ')
            if parts[0] == '#':
                if len(graph) > 0:
                    graphs.append(graph)
                    graph = []
            else:
                if len(filename_parts)>=2:
                    
                    if filename_parts[1] == 'safety':
                        path = tuple([int(x) for x in parts[0:(len(parts))]])
                    elif filename_parts[1] == 'catfish':
                        path = tuple([int(x) for x in parts[7:(len(parts))]])
                    elif filename_parts[0] == 'data':
                        path = tuple([int(x) for x in parts[1:(len(parts))]])
                    else:
                        print('invalid filetype')
                        break
                else:
                    if type == 'safety':
                        path = tuple([int(x) for x in parts[0:(len(parts))]])
                    elif type == 'catfish':
                        path = tuple([int(x) for x in parts[7:(len(parts))]])
                    elif type == 'truth':
                        path = tuple([int(x) for x in parts[1:(len(parts))]])
                    else:
                        print('invalid filetype')
                        break
                graph.append(path)
    graphs.append(graph)
    return graphs