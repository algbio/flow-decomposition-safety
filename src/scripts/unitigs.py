'''
Class for computing unitigs
'''
#!/usr/bin/python3
import argparse
from src.scripts.main import flow_decomposition, to_vertex_list
from src.scripts import io_helper


def main(input_file, mode):
    graphs = io_helper.read_gfa_file(input_file)
    i = 0
    for g in graphs:
        print(f'# graph {i}')
        decomposition_paths = flow_decomposition(g)
        unitgs_set = set()
        for path in decomposition_paths:
            list = get_unitigs(path, g)
            for x in list:
                unitgs_set.add(x)
        print(unitgs_set)
        i += 1


def get_unitigs(path, graph):
    unitigs = []
    vertex_path = to_vertex_list(path)
    unitig = []
    last_added = -1
    for (i, v) in enumerate(vertex_path[1:-1], start=1):
        if graph.out_degree(v) == 1 and graph.in_degree(v) == 1:
            if last_added == i-1:
                # last vertex was added, unitig continues
                unitig.append(v)
            else:
                # last vertex wasn't added
                # add last constructed unitig
                if unitig:
                    unitig.append(vertex_path[last_added+1])
                    unitigs.append(tuple(unitig))
                # begin new unitig
                unitig = [vertex_path[i-1], v]
            last_added = i
    if unitig:
        unitig.append(vertex_path[last_added+1])
        unitigs.append(tuple(unitig)) 
    return unitigs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--graph_file", help="path to input file")
    parser.add_argument("-m", "--mode",
                        help="Default mode outputs path file, mode 'indices' outputs file with flow decomposition and indices of safe paths", default=None)
    args = parser.parse_args()

    file = args.graph_file
    main(args.graph_file, args.mode)
