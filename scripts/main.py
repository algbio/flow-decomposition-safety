#!/usr/bin/python3
import networkx as nx
from networkx.algorithms.flow import edmonds_karp
from networkx.algorithms.flow import shortest_augmenting_path
from networkx.classes.function import neighbors
from networkx.generators.classic import path_graph


def main():
    file = 'data/test.gfa'
    graph = read_graph(file)
    # graph.edges[0,1]['capacity'] = 1
    # print(graph.edges[0,1])
    # print(graph)
    # paths = read_paths(file)
    # print(paths)
    comp = flow_decomposition(graph, 0, 4)
    print(comp)
    # dfs(graph, [0], 0, 7)


def read_graph(filename):
    # save graph
    graph = nx.DiGraph()
    with open(filename, 'r') as f:
        for line in f:
            # read line
            read = ''
            if line.rstrip().count('\t') > 0:
                read = (line.rstrip()).split('\t')
            else:
                read = (line.rstrip()).split(' ')

            # add edge
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


def flow_decomposition(graph, s, t):
    stack = [s]
    min_flow = 9999
    path = []
    paths = []
    while(len(stack) > 0):
        v = stack.pop()
        if v == t:
            paths.append(path)

            for e in path:
                graph.edges[e[0], e[1]]['capacity'] -= min_flow
            path = []
            min_flow = 9999
            stack.append(s)
            cap = 0
            for p in graph.predecessors(t):
                cap += graph.edges[p, t]['capacity']
            if cap == 0:
                return paths
        else:
            max_route = 0
            max_flow = 0
            for n in graph.neighbors(v):
                if graph.edges[v, n]['capacity'] > max_flow:
                    max_flow = graph.edges[v, n]['capacity']
                    max_route = n
            stack.append(max_route)
            path.append((v, max_route))
            if graph.edges[v, max_route]['capacity'] < min_flow:
                min_flow = graph.edges[v, max_route]['capacity']


def dfs(graph, path, paths, s, t):
    if s == t:
        print(path)
        return paths
    for n in list(graph.neighbors(s)):
        path.append(n)
        dfs(graph, path, n, t)


if __name__ == '__main__':
    main()
