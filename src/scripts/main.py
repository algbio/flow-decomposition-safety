'''
Main class for safety algorithm
'''
#!/usr/bin/python3
import argparse
from src.scripts import io_helper


def main(input_file, output_file):
    graphs = io_helper.read_gfa_file(input_file)
    i = 0
    for g in graphs:
        io_helper.write_file(f'# graph {i}\n', output_file)
        result = maximal_safety(g)
        io_helper.write_file(f'{result}\n', output_file)
        i += 1


def excess_flow(graph, path):
    '''
    excess_flow(self, path) -> int
    Calculates the excess flow  of the given path. 
    Returns value of excess flow.
    '''
    flow_sum = 0
    flow_out_sum = 0
    for i in range(1,len(path)):
        flow_sum += graph.edges[path[i-1],path[i]]['weight']
        flow_out_sum += graph.nodes[path[i-1]]['flow_out']
    return flow_sum - (flow_out_sum - graph.nodes[path[0]]['flow_out'])


def safety_of_path(graph, path, w):
    '''
    safety_of_path(self, path, w) -> Boolean
    If the given path is w-safe returns true else return false.
    '''
    return excess_flow(graph, path) >= w and w > 0


def maximal_safety_indices(graph, in_flow_decomposition=None, timers=False):
    '''
    maximal_safety(self, flow_decomposition) -> list of indices (one to one relation to flow decomposition)
    Uses maximal safety algorithm (by Shahbaz, Tomescu) to compute a list of indices for given flow decomposition.
    in_flow_decomposition parameter is used for testing.
    timer parameter is used measuring the execution of algorithm
    TODO: returning list could be dictionary (key flow decomposition, value indices)
    TODO: paths could be represented a vertice list
    '''
    flow_decomposition_paths = []
    if not in_flow_decomposition:
        flow_decomposition_paths = flow_decomposition(graph)
    else:
        flow_decomposition_paths = in_flow_decomposition
    list_safety_indices = []
    for path in flow_decomposition_paths:
        safety_indices = []
        start = 0
        end = 1
        f = excess_flow(graph, path[0:3])
        added = False
        while True:
            if end == len(path)-1 and f > 0:
                if end-start >= 2:
                    safety_indices.append((start, end-1))
                break
            if f > 0:
                end += 1
                f_out = graph.nodes[path[end]]['flow_out']
                f -= (f_out - graph.edges[(path[end-1],path[end])]['weight'])
                added = False
            else:
                if not added:
                    if end-start >= 2:
                        safety_indices.append((start, end-2))
                    added = True

                start += 1
                f_in = graph.nodes[path[start]]['flow_in']
                f += (f_in - graph.edges[(path[start-1],path[start])]['weight'])
        list_safety_indices.append(safety_indices)
    return list_safety_indices


def maximal_safety(graph, in_flow_decomposition=None):
    '''
    maximal_safety(self, flow_decomposition) -> list of paths
    Uses maximal safety algorithm (by Shahbaz, Tomescu) to compute a list of paths.
    Paths are represented as list of edges.
    in_flow_decomposition parameter is used for testing.
    '''
    safe_paths = []
    flow_decomposition_paths = []
    if not in_flow_decomposition:
        flow_decomposition_paths = flow_decomposition(graph)
    else:
        flow_decomposition_paths = in_flow_decomposition
    for path in flow_decomposition_paths:
        sub = path[0:3]
        f = excess_flow(graph, sub)
        i = 2
        added = False
        while True:
            if i == len(path)-1 and f > 0:
                if len(sub) >= 3:
                    safe_paths.append(sub)
                break
            if f > 0:
                i += 1
                f_out = graph.nodes[path[i]]['flow_out']
                f -= (f_out - graph.edges[path[i-1],path[i]]['weight'])
                sub.append(path[i])
                added = False
            else:
                first = sub[0]
                if not added:
                    if len(sub[0:-2]) >= 3:
                        safe_paths.append(sub[0:-2])
                    added = True
                sub = sub[1:len(sub)]
                f_in = graph.nodes[sub[0]]['flow_in']
                f += (f_in - graph.edges[first,sub[0]]['weight'])
    return safe_paths


def flow_decomposition(graph):
    '''
    flow_decomposition(self)->list of paths
    Calculates a flow decomposition for the graph.
    Returns list of paths as list of edges (tuples).
    '''
    paths = []
    v = graph.graph['source']
    min_flow = float('inf')
    path = []
    cap = graph.nodes[graph.graph['source']]['flow_out']
    while(True):
        if v == graph.graph['sink']:
            path.append(v)
            paths.append(path)
            for i in range(1,len(path)):
                graph.edges[(path[i-1],path[i])]['weight_copy'] -= min_flow
            cap -= min_flow
            if cap == 0:
                break
            path = []
            min_flow = float('inf')
            v = graph.graph['source']
        else:
            (v1,v2,dic) = [(i,j,k) for i,j,k in graph.out_edges(v, data=True) if k['weight_copy'] > 0][0]
            if dic['weight_copy'] < min_flow:
                min_flow = dic['weight_copy']
            path.append(v2)
            v = v2
    return paths


def safe_paths_to_string(paths):
    '''
    safe_paths_to_string(self) -> string edgelist of the paths generated by safety algorithm
    '''
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--graph_file", help="path to input file")
    parser.add_argument("-o", "--output_file", help="path to output file")
    parser.add_argument("-m", "--mode",
                        help="Default mode outputs path file, mode 'indices' outputs file with flow decomposition and indices of safe paths", default=None)
    args = parser.parse_args()

    file = args.graph_file
    main(args.graph_file, args.output_file)
