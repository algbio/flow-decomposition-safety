#!/usr/bin/python3
import networkx as nx


class Graph:
    def __init__(self, graph):
        self.graph = graph

    def excess_flow(self, path):
        flow_sum = 0
        flow_out_sum = 0
        for e in path:
            flow_sum += self.graph.edges[e]['capacity']
            flow_out_sum += self.graph.nodes[e[0]]['flow_out']
        return flow_sum - (flow_out_sum - self.graph.nodes[path[0][0]]['flow_out'])

    def safety_of_path(self, path, w):
        return self.excess_flow(path) >= w and w > 0

    def maximal_safe_paths(self, paths):
        max_safe_paths = []
        for path in paths:
            sub = [path[0], path[1]]
            f = self.excess_flow(sub)
            i = 1
            while True:
                if i == len(path)-1 and f > 0:
                    max_safe_paths.append(sub)
                    break
                if f > 0:
                    i += 1
                    f_out = self.graph.nodes[path[i][0]]['flow_out']
                    f -= (f_out - self.graph.edges[path[i]]['capacity'])
                    sub.append(path[i])
                else:
                    first = sub[0]
                    sub = [x for x in sub[1:len(sub)]]
                    f_in = self.graph.nodes[sub[0][0]]['flow_in']
                    f += (f_in - self.graph.edges[first]['capacity'])
        return max_safe_paths


def main():
    file = 'data/graph.gfa'
    graph = read_graph(file)
    g = Graph(graph)
    composed_paths = flow_decomposition(graph.copy(), 0, 13)
    print("composed paths")
    for p in composed_paths:
        print(p)
    print("*****")
    max_safe_paths = g.maximal_safe_paths(composed_paths)
    print("maximum safe paths:")
    for p in max_safe_paths:
        print(p)


def read_graph(filename):
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
                graph.edges[e]['capacity'] -= min_flow

            path = []
            min_flow = 9999
            stack = [s]

            cap = 0
            for e in graph.out_edges(s):
                cap += graph.edges[e]['capacity']
            if cap == 0:
                return paths
        else:
            max_route = 0
            max_flow = 0
            for e in graph.out_edges(v):
                if graph.edges[e]['capacity'] > max_flow:
                    max_flow = graph.edges[e]['capacity']
                    max_route = e[1]
            stack.append(max_route)
            path.append((v, max_route))

            if graph.edges[v, max_route]['capacity'] < min_flow:
                min_flow = graph.edges[v, max_route]['capacity']


if __name__ == '__main__':
    main()
