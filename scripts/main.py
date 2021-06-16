#!/usr/bin/python3
import networkx as nx
import argparse
import os
import io_helper
from timeit import default_timer as timer


class Graph:
    def __init__(self, graph, s, t, debug=False):
        self.graph = graph
        self.s = s
        self.t = t
        self.debug = debug
        self.flow_decomposition_paths = []
        self.max_safe_paths = []

    def excess_flow(self, path):
        flow_sum = 0
        flow_out_sum = 0
        for e in path:
            flow_sum += self.graph.edges[e]['capacity']
            flow_out_sum += self.graph.nodes[e[0]]['flow_out']
        return flow_sum - (flow_out_sum - self.graph.nodes[path[0][0]]['flow_out'])

    def safety_of_path(self, path, w):
        return self.excess_flow(path) >= w and w > 0

    def maximal_safe_paths(self):
        self.flow_decomposition()
        for path in self.flow_decomposition_paths:
            if self.debug:
                print('decomposition in processing')
                print(path)
            sub = [path[0], path[1]]
            f = self.excess_flow(sub)
            i = 1
            added = False
            if self.debug:
                print(f'setting up subpath {sub}')
                print(f'flow {f}')
                print(f'i: {i}')
                print('*********')
            while True:
                if i == len(path)-1 and f > 0:
                    if len(sub) >= 2:
                        self.max_safe_paths.append(sub)
                        if self.debug:
                            print(f'MAX SAFE PATH ADDED {sub}')
                            print(f'and flow was {f}')
                    break
                if f > 0:
                    i += 1
                    f_out = self.graph.nodes[path[i][0]]['flow_out']
                    f -= (f_out - self.graph.edges[path[i]]['capacity'])
                    sub.append(path[i])
                    added = False
                    if self.debug:
                        print('my flow is positive')
                        print(f'i (index in path) is now{i}')
                        print(f'flow out is {f_out}')
                        print(f'flow {f}')
                        print(f'Sub is now f{sub}')
                        print('*********')
                else:
                    if self.debug:
                        print('my flow is negative')
                    first = sub[0]
                    if not added:
                        if len(sub) >= 2:
                            if self.debug:
                                print(f'MAX SAFE PATH ADDED {sub}')
                            self.max_safe_paths.append(sub)
                        added = True
                    sub = [x for x in sub[1:len(sub)]]
                    f_in = self.graph.nodes[sub[0][0]]['flow_in']
                    f += (f_in - self.graph.edges[first]['capacity'])
                    if self.debug:
                        print(f'i (index in path) is now{i}')
                        print(f'flow in is {f_in}')
                        print(f'flow {f}')
                        print(f'Sub is now f{sub}')
                        print('*********')
        return self.max_safe_paths

    def flow_decomposition(self):
        v = self.s
        min_flow = float('inf')
        path = []
        copy_of_graph = self.graph.copy()

        cap = copy_of_graph.nodes[self.s]['flow_out']

        while(True):
            if v == self.t:
                self.flow_decomposition_paths.append(path)
                rmv = []
                for e in path:
                    copy_of_graph.edges[e]['capacity'] -= min_flow
                    if copy_of_graph.edges[e]['capacity'] == 0:
                        rmv.append(e)
                copy_of_graph.remove_edges_from(rmv)
                path = []
                cap -= min_flow
                min_flow = float('inf')
                v = self.s
                if cap == 0:
                    break
            else:
                next = list(copy_of_graph.successors(v))[0]
                if copy_of_graph.edges[v, next]['capacity'] < min_flow:
                    min_flow = copy_of_graph.edges[v, next]['capacity']
                path.append((v, next))
                v = next
        return self.flow_decomposition_paths

    def print(self):
        print(self)

    def __str__(self):
        return (f'source: {self.s}\n'
                f'sink: {self.t}\n'
                f'graph: {list(self.graph.edges)}\n'
                f'flow decomposition: {self.flow_decomposition_paths}\n'
                f'maximum safe paths: {self.max_safe_paths}\n')


def main():
    if os.path.isfile('data/output.txt'):
        os.remove('data/output.txt')
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--graph_file", help="path to file")
    parser.add_argument("-o", "--output_file", help="path to file")
    parser.add_argument("-s", "--source", type=int, default=-1,
                        help="source of graph. optional")
    parser.add_argument("-t", "--sink", type=int, default=-1,
                        help="sink of graph, optional")
    parser.add_argument("--number_of_graphs", type=int,
                        help="number of graphs to read. can be used if file contains many graphs")
    args = parser.parse_args()

    file = args.graph_file
    graphs = read_file(file)
    i = 0
    for g in graphs:
        g.print()
        max = g.maximal_safe_paths()
        g.print()
        io_helper.write_file(f'# graph {i}', args.output_file)
        for m in max:
            io_helper.write_file(path_to_string(m), args.output_file)
        i += 1


def read_file(filename):
    graphs = []
    graph = None
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            # read line
            read = (line.rstrip()).split('\t')
            # add edge
            if line[0] == 'H':
                if i != 0:
                    graphs.append(Graph(graph, 0, len(graph.nodes)-1))
                graph = nx.DiGraph()
            if line[0] == 'L':
                v_from = int(read[1])
                v_to = int(read[3])
                weight = int((read[5])[0:-1])
                graph.add_edge(v_from, v_to, capacity=weight)
                init_node(graph.nodes, v_from, v_to, weight)
    if graph is not None:
        graphs.append(Graph(graph, 0, len(graph.nodes)-1))
    return graphs


def init_node(nodes, v_from, v_to, weight):
    if 'flow_out' not in nodes[v_from]:
        nodes[v_from]['flow_out'] = 0
    if 'flow_out' not in nodes[v_to]:
        nodes[v_to]['flow_out'] = 0
    if 'flow_in' not in nodes[v_from]:
        nodes[v_from]['flow_in'] = 0
    if 'flow_in' not in nodes[v_to]:
        nodes[v_to]['flow_in'] = 0
    nodes[v_to]['flow_in'] += weight
    nodes[v_from]['flow_out'] += weight


def calc_source(nodes):
    for n in nodes:
        if is_source(nodes, n):
            return n
    return 0


def calc_sink(nodes):
    for n in nodes:
        if is_sink(nodes, n):
            return n
    return len(nodes)-1


def is_source(nodes, v):
    return nodes[v]['flow_in'] == 0


def is_sink(nodes, v):
    return nodes[v]['flow_out'] == 0


def path_to_string(path):
    str = ''
    i = 0
    for p in path:
        str += f'{p[0]} '
        if i == len(path)-1:
            str += f'{p[1]}'
        i += 1
    return str


if __name__ == '__main__':
    main()
