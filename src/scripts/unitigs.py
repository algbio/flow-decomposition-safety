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
    offset = 1
    for g in graphs:
        print(f'# graph {i}')
        decomposition_paths = flow_decomposition(g)
        # unitigs are saved to set because it's no
        unitgs_set = set()
        for path in decomposition_paths:
            vertex_path = to_vertex_list(path)
            if not mode:
                enum = enumerate(vertex_path[1:-1], start=1)
                pre = lambda out_degree, in_degree: out_degree == 1 and in_degree == 1
                list = get_unitigs(vertex_path, g, enum, pre, offset)
            else: 
                enum = enumerate(vertex_path[1:-1], start=1)
                pre = lambda out_degree, in_degree: out_degree == 1
                r_enum = reverse_enumerator(vertex_path[1:-1], start=1)
                r_pre = lambda out_degree, in_degree: in_degree == 1
                list = get_unitigs(vertex_path, g, enum, pre, offset) + get_unitigs(vertex_path, g, r_enum, r_pre, -offset)
            for x in list:
                unitgs_set.add(tuple(x))
        print(unitgs_set)
        i += 1


def get_unitigs(vertex_path, graph, enumerator, predicate, offset):
    unitigs = []
    unitig = []
    last_added = -1
    for (i, v) in enumerator:
        if predicate(graph.out_degree(v), graph.in_degree(v)):
            if last_added == i-offset:
                # last vertex was added, unitig continues
                unitig.append(v)
            else:
                # last vertex wasn't added
                # add last constructed unitig
                if unitig:
                    unitig.append(vertex_path[last_added+offset])
                    if offset<0:
                        unitig.reverse()
                    unitigs.append(unitig)
                # begin new unitig
                unitig = [vertex_path[i-offset], v]
            last_added = i
    if unitig:
        unitig.append(vertex_path[last_added+offset])
        if offset<0:
            unitig.reverse()
        unitigs.append(unitig)
    return unitigs

def reverse_enumerator(l, start=0):
    for i in range(len(l)-1,-1,-1):
        yield (i+start, l[i])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--graph_file", help="path to input file")
    parser.add_argument(
        "-m", "--mode", help="mode of unitigs computation. If given computes modified unitigs else default unitigs are computed", default=None)
    args = parser.parse_args()

    file = args.graph_file
    main(args.graph_file, args.mode)
