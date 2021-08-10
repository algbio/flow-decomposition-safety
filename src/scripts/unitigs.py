'''
Class for computing unitigs
'''
# !/usr/bin/python3
import argparse
from src.scripts.main import flow_decomposition, to_vertex_list
from src.scripts import io_helper


# Something for you to know: computing unitigs and unitigs++ should not require to compute a flow_decomposition,
# because the definition of them does not require the decomposition and computing this is computationally more expensive
# than just computing the unitigs or unitigs++
# Computing the unitigs in the correct time complexity is a bit trickier than what we did here, but we should not worry
# about that unless we are also interested in comparing the time to get these unitigs.

def main(input_file, mode):  # Nice way of solving the problem, great!
    graphs = io_helper.read_gfa_file(input_file)
    i = 0
    offset = 1
    for g in graphs:  # The i = 0 and i +=1 from the end can be replaced here by doing for i, g in enumerate(graphs):
        print(f'# graph {i}')
        decomposition_paths = flow_decomposition(g)
        # unitigs are saved to set because it eliminates duplicate paths
        unitgs_set = set()  # Great that you realized this. The issue is actually more profound. We should not report
        # unitigs that are subpaths of other unitigs reported, because we would bias the metrics (in the results) if
        # we do so. If we think for a moment we realize that the only way that this could happen is that there is an
        # overlap between two flow paths in the flow decomposition, such that the overlap contains a unitig, and this
        # unitig can be extended through one path but not through the other, as such we would report one unitig that is
        # subpath of the other, an error that is not solved by maintaining the paths in a set().
        # In the case of unitigs and unitigs++ I think this won't happen because of their definition (this is no simple
        # to se), thus your code should be correct. However, in the case of maximal safe paths this could happen,
        # and I think we are not dealing with this possible error there now, that is, we report safe paths that are
        # maximal for each path in the flow decomposition, but some of these paths could be subpath (or even the same)
        # than another reported safe path.
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
                list = get_unitigs(vertex_path, g, enum, pre, offset) + get_unitigs(vertex_path, g, r_enum, r_pre,
                                                                                    -offset)
            for x in list:  # A cool way to do this is just x.update(set(list))
                unitgs_set.add(tuple(x))
        print(unitgs_set)
        i += 1


def get_unitigs(vertex_path, graph, enumerator, predicate, offset):
    unitigs = []
    unitig = []
    last_added = -1
    for (i, v) in enumerator:
        if predicate(graph.out_degree(v), graph.in_degree(v)):
            if last_added == i - offset:
                # last vertex was added, unitig continues
                unitig.append(v)
            else:
                # last vertex wasn't added
                # add last constructed unitig
                if unitig:
                    unitig.append(vertex_path[last_added + offset])
                    if offset < 0:
                        unitig.reverse()
                    unitigs.append(unitig)
                # begin new unitig
                unitig = [vertex_path[i - offset], v]
            last_added = i
    if unitig:
        unitig.append(vertex_path[last_added + offset])
        if offset < 0:
            unitig.reverse()
        unitigs.append(unitig)
    return unitigs


def reverse_enumerator(l, start=0):
    for i in range(len(l) - 1, -1, -1):
        yield (i + start, l[i])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--graph_file", help="path to input file")
    parser.add_argument(
        "-m", "--mode",
        help="mode of unitigs computation. If given computes modified unitigs else default unitigs are computed",
        default=None)
    args = parser.parse_args()

    file = args.graph_file
    main(args.graph_file, args.mode)
