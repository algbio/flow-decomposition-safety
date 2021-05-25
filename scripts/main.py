#!/usr/bin/python3
import networkx as nx
from networkx.algorithms.flow import edmonds_karp
from networkx.algorithms.flow import shortest_augmenting_path

def main():
    file = 'data/dag_graph.gfa'
    graph = read_graph(file)
    # print(graph)
    paths = read_paths(file)
    # print(paths)
    #all_max_safe_paths(paths)
    ff = nx.maximum_flow(graph, 0, 7)
    print(ff)


def read_graph(filename):
    # save graph as a adjacency list
    graph = nx.Graph()
    with open(filename, 'r') as f:
        for line in f:
            # read line
            read = ''
            if line.rstrip().count('\t') > 0:
                read = (line.rstrip()).split('\t')
            else:
                read = (line.rstrip()).split(' ')

            # add edge to the adjecency list
            if line[0] == 'L':
                v_from = int(read[1])
                v_to = int(read[3])
                weight = int((read[5])[0:-1])
                graph.add_edge(v_from, v_to, capacity=weight)
    return graph

def read_paths(filename):
    paths = []
    with open(filename, 'r') as f:
        for line in f:
            if line[0] == 'P':
                paths.append(line.rstrip())
    return paths

if __name__ == '__main__':
    main()
