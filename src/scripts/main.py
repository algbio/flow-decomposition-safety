'''
Main class for safety algorithm
'''
#!/usr/bin/python3
import argparse
from src.scripts import io_helper


def main(input_file, mode):
    #graphs = io_helper.read_gfa_file(input_file)
    graphs = io_helper.read_sg_file(input_file)
    i = 0
    for g in graphs:
        print(f'# graph {i}')
        result_paths = maximal_safety(g) if not mode else maximal_safety_indices(g)
        for j, path in enumerate(sorted(result_paths, key=lambda x: len(x), reverse=True)):
            if mode == '1':
                if result_paths[path] != []:
                    print(path_to_string(path))
                    print(safety_indices_to_string(result_paths[path]))
            elif mode == '2':
                if check_unique(path, [x for x in result_paths if x != path]):
                    print(path_to_string(path))
            else:
                print(path_to_string(path))
        i += 1

def check_unique(path, paths):
    for p in paths:
        if path_to_string(path) in path_to_string(p):
            return False
    return True

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
    '''
    flow_decomposition_paths = flow_decomposition(graph) if not in_flow_decomposition else in_flow_decomposition
    list_safety_indices = {}
    for path in flow_decomposition_paths:
        safety_indices = []
        start = 0
        end = 1
        f = excess_flow(graph, [path[0], path[1]])

        added = False
        while True:
            if end == len(path)-1 and f > 0:
                if end-start >= 1 and (start,end) not in safety_indices:
                    safety_indices.append((start, end))
                break
            if f > 0:
                end += 1
                f_out = graph.nodes[path[end][0]]['flow_out']
                f -= (f_out - graph.edges[path[end]]['weight'])
                added = False
            else:
                if not added:
                    if end-start >= 2 and (start,end) not in safety_indices:
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
    flow_decomposition_paths = flow_decomposition(graph) if not in_flow_decomposition else in_flow_decomposition

    for path in flow_decomposition_paths:
        sub = [path[0], path[1]]
        f = excess_flow(graph, sub)
        i = 1
        added = False
        while True:
            if i == len(path)-1 and f > 0:
                if len(sub) >= 2 and sub not in safe_paths:
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
                    if len(sub[0:-1]) >= 2 and sub[0:-1] not in safe_paths:
                        safe_paths.append(sub[0:-1])
                    added = True
                sub = sub[1:len(sub)]
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

def to_vertex_list(path):
    verteces = [e[0] for e in path] 
    verteces.append(path[-1][-1])
    return verteces

def path_to_string(path):
    return " ".join(str(x) for x in to_vertex_list(path))

def edge_indices_to_vertex_indices(safety_indices_list):
    return [(v1,v2+1) for v1,v2 in safety_indices_list]

def safety_indices_to_string(safety_indices_list):
    return ''.join(str(x) for x in edge_indices_to_vertex_indices(safety_indices_list))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--graph_file", help="path to input file")
    parser.add_argument("-m", "--mode",
                        help="Default mode outputs path file, mode 'indices' outputs file with flow decomposition and indices of safe paths", default=None)
    args = parser.parse_args()

    file = args.graph_file
    main(args.graph_file, args.mode)
