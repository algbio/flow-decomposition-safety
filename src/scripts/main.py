'''
Main class for safety algorithm
'''
#!/usr/bin/python3
import argparse
from src.scripts import io_helper


def main(input_file, output_file, mode):
    graphs = io_helper.read_gfa_file(input_file)
    i = 0
    for g in graphs:
        io_helper.write_file(f'# graph {i}\n', output_file)
        result = maximal_safety(g) if not mode else maximal_safety_indices(g)
        io_helper.write_file(safe_paths_to_string(result, mode), output_file)
        i += 1


def excess_flow(graph, path):
    '''
    excess_flow(self, path) -> int
    Calculates the excess flow  of the given path. 
    Returns value of excess flow.
    '''
    flow_sum = 0
    flow_out_sum = 0
    for e in path:
        flow_sum += graph.edges[e]['weight']
        flow_out_sum += graph.nodes[e[0]]['flow_out']
    return flow_sum - (flow_out_sum - graph.nodes[path[0][0]]['flow_out'])


def safety_of_path(graph, path, w):
    '''
    safety_of_path(self, path, w) -> Boolean
    If the given path is w-safe returns true else return false.
    '''
    return excess_flow(graph, path) >= w and w > 0


def maximal_safety_indices(graph, in_flow_decomposition=None):
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
    list_safety_indices = {}
    for path in flow_decomposition_paths:
        safety_indices = []
        start = 0
        end = 1
        f = excess_flow(graph, [path[0], path[1]])

        added = False
        while True:
            if end == len(path)-1 and f > 0:
                if end-start >= 2:
                    safety_indices.append((start, end))
                break
            if f > 0:
                end += 1
                f_out = graph.nodes[path[end][0]]['flow_out']
                f -= (f_out - graph.edges[path[end]]['weight'])
                added = False
            else:
                if not added:
                    if end-start >= 2:
                        safety_indices.append((start, end))
                    added = True

                start += 1
                f_in = graph.nodes[path[start][0]]['flow_in']
                f += (f_in - graph.edges[(path[start-1])]['weight'])
        list_safety_indices[tuple(path)] = safety_indices
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
        sub = [path[0], path[1]]
        f = excess_flow(graph, sub)
        i = 1
        added = False
        while True:
            if i == len(path)-1 and f > 0:
                if len(sub) >= 2:
                    safe_paths.append(sub)
                break
            if f > 0:
                i += 1
                f_out = graph.nodes[path[i][0]]['flow_out']
                f -= (f_out - graph.edges[path[i]]['weight'])
                sub.append(path[i])
                added = False
            else:
                first = sub[0]
                if not added:
                    if len(sub[0:-1]) >= 2:
                        safe_paths.append(sub[0:-1])
                    added = True
                sub = [x for x in sub[1:len(sub)]]
                f_in = graph.nodes[sub[0][0]]['flow_in']
                f += (f_in - graph.edges[first]['weight'])
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
            paths.append(path)
            for e in path:
                graph.edges[e]['weight_copy'] -= min_flow
            path = []
            cap -= min_flow
            min_flow = float('inf')
            v = graph.graph['source']
            if cap == 0:
                break
        else:
            (v1,v2,dic) = [(i,j,k) for i,j,k in graph.out_edges(v, data=True) if k['weight_copy'] > 0][0]
            if dic['weight_copy'] < min_flow:
                min_flow = dic['weight_copy']
            path.append((v, v2))
            v = v2
    return paths


def safe_paths_to_string(paths, mode):
    '''
    safe_paths_to_string(paths, mode) -> string 
    edgelist of the paths generated by safety algorithm
    '''
    if not mode:
        str = ''
        for path in paths:
            str += path_to_string(path)
        return str
    else:
        str = ''
        for i in paths:
            str += f'{i}\n'
            str += f'{paths[i]}\n'
        return str

        

def path_to_string(path):
    str = ''
    for (i, edge) in enumerate(path):
        str += f'{edge[0]} '
        if i == len(path)-1:
            str += f'{edge[1]}\n'
    return str


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--graph_file", help="path to input file")
    parser.add_argument("-o", "--output_file", help="path to output file")
    parser.add_argument("-m", "--mode",
                        help="Default mode outputs path file, mode 'indices' outputs file with flow decomposition and indices of safe paths", default=None)
    args = parser.parse_args()

    file = args.graph_file
    main(args.graph_file, args.output_file, args.mode)
