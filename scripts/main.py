#!/usr/bin/python3
import networkx as nx
from networkx.algorithms.flow import edmonds_karp
from networkx.algorithms.flow import shortest_augmenting_path
from networkx.algorithms.flow.maxflow import maximum_flow
from networkx.classes import graph
from networkx.classes.function import neighbors
from networkx.generators.classic import path_graph
from networkx.generators.trees import prefix_tree
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, graph, s, t):
        self.graph = graph
        self.s = s
        self.t = t

    def excess_flow(self, path):
        flow_sum = 0
        flow_out_sum = 0
        for e in path:
            flow_sum += self.graph.edges[e[0], e[1]]['capacity']
            if path[0][0] != e[0]:
                flow_out_sum += self.graph.nodes[e[0]]['flow_out']
        return flow_sum - flow_out_sum

    def safety_of_path(self, path, w):
        return self.excess_flow(path) >= w and w > 0

    def maximal_safe_paths(self, paths):
        max_safe_paths = []
        for p in paths:
            sub = [p[0], p[1]]
            f = self.excess_flow(sub)
            i = 1
            while True:
                if i == len(p)-1 and f > 0:
                    max_safe_paths.append(sub)
                    break
                if f > 0:
                    i += 1
                    f_out = self.graph.nodes[p[i][0]]['flow_out']
                    f -= (f_out - self.graph.edges[p[i]]['capacity'])
                    sub.append(p[i])
                else:
                    first = sub[0]
                    sub = [x for x in sub[1:len(sub)]]
                    f_in = self.graph.nodes[sub[0][0]]['flow_in']
                    f += (f_in-self.graph.edges[first]['capacity'])
        return max_safe_paths


def main():
    file = 'data/graph.gfa'
    graph = read_graph(file)
    g = Graph(graph, 0, 13)
    composed_paths = flow_decomposition(graph.copy(), 0, 13)
    max_safe_paths = g.maximal_safe_paths(composed_paths)


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
                if 'flow_out' not in graph.nodes[v_from]:
                    graph.nodes[v_from]['flow_out'] = 0
                if 'flow_out' not in graph.nodes[v_to]:
                    graph.nodes[v_to]['flow_out'] = 0
                if 'flow_in' not in graph.nodes[v_from]:
                    graph.nodes[v_from]['flow_in'] = 0
                if 'flow_in' not in graph.nodes[v_to]:
                    graph.nodes[v_to]['flow_in'] = 0

                graph.nodes[v_to]['flow_in'] += weight
                graph.nodes[v_from]['flow_out'] += weight
    return graph

#not used


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
            stack = [s]
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


def two_pointer_scan(paths):
    pass


if __name__ == '__main__':
    main()
