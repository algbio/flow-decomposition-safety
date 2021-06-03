#!/usr/bin/python3
import networkx as nx


class Graph:
    def __init__(self, graph, n=0, s=0, t=0):
        self.graph = graph
        self.n = n
        self.s = s
        self.t = t
        if n != 0:  #Ariel: It's strange that this case is treated in the constructor, I think it should be treated when calling the constructor not on it
            self.s = 0
            self.t = n-1

    def excess_flow(self, path):
        flow_sum = 0
        flow_out_sum = 0
        for e in path:
            flow_sum += self.graph.edges[e]['capacity']
            flow_out_sum += self.graph.nodes[e[0]]['flow_out']
        return flow_sum - (flow_out_sum - self.graph.nodes[path[0][0]]['flow_out'])

    def safety_of_path(self, path, w):
        return self.excess_flow(path) >= w and w > 0

    def maximal_safe_paths(self, paths):  #Ariel: We could add an initial comment to this function since it isn't trivial what it does at first sight, something like, 'it finds the maximal safe paths given a flow decomposition by the method explained at... it returns the paths as a...'
        max_safe_paths = []
        for path in paths:
            sub = [path[0], path[1]]
            f = self.excess_flow(sub)
            i = 1
            added = False
            while True:
                if i == len(path)-1 and f > 0:
                    max_safe_paths.append(sub)
                    break
                if f > 0:
                    i += 1
                    f_out = self.graph.nodes[path[i][0]]['flow_out']
                    f -= (f_out - self.graph.edges[path[i]]['capacity'])
                    sub.append(path[i])
                    added = False
                else:
                    first = sub[0]
                    if not added:
                        max_safe_paths.append(sub) #Ariel: I'm not sure about this but I think that there is a 'off-by-one error' here, this because if we are in this else, then the excess_flow of 'sub' should be <= 0, thus sub is not safe. Please check this.
                        added = True
                    sub = [x for x in sub[1:len(sub)]]  #Ariel: Recall to use a linked list or a pair of indices to represent the paths. I personally prefer the pair of indices because you can use the decomposition to recover the paths in any format you want them
                    f_in = self.graph.nodes[sub[0][0]]['flow_in']
                    f += (f_in - self.graph.edges[first]['capacity'])
        return max_safe_paths

    def flow_decomposition(self):  #Ariel: We could add an initial comment to this function since it isn't trivial what it does at first sight, something like, 'it finds a flow decomposition with the following method... it returns the paths as a list of sequence of edges'
        stack = [self.s]
        min_flow = 999999  #Ariel: A more elegant way to do this is float('inf')
        path = []
        paths = []
        copy_of_graph = self.graph.copy()

        while(len(stack) > 0):  #Ariel: A cool way to do this in python is just 'while stack:'
            v = stack.pop()     #Ariel: Also, I do not think it's necessary to use a stack here, since this always contains at most one element

            if v == self.t:
                paths.append(path)
                for e in path:
                    copy_of_graph.edges[e]['capacity'] -= min_flow

                path = []
                min_flow = 9999   #Ariel: This is different from the one above
                stack = [self.s]

                cap = 0
                for e in copy_of_graph.out_edges(self.s):
                    cap += copy_of_graph.edges[e]['capacity']
                if cap == 0:
                    return paths
            else:
                max_route = 0
                max_flow = 0
                for e in copy_of_graph.out_edges(v):
                    if copy_of_graph.edges[e]['capacity'] > max_flow:
                        max_flow = copy_of_graph.edges[e]['capacity']
                        max_route = e[1]
                stack.append(max_route)
                path.append((v, max_route))

                if copy_of_graph.edges[v, max_route]['capacity'] < min_flow:
                    min_flow = copy_of_graph.edges[v, max_route]['capacity']

    def print(self):
        for e in self.graph.edges:
            print(e, ' capacity: ', self.graph.edges[e]['capacity'])


def main():
    file = 'data/1.graph'
    graphs = read_graph(file, 6)
    i = 0
    for g in graphs:
        print('graph')
        g.print()
        print('decomposition')
        dec = g.flow_decomposition()
        for d in dec:
            print(d)
        i += 1
        print('max safe paths')
        max_safe = g.maximal_safe_paths(dec)
        for p in max_safe:
            print(p)
        print('***************')
        print('example:')
        file = 'data/graph.gfa'
        graph = read_graph(file)
        g = Graph(graph, 0, 0, 13)
        composed_paths = g.flow_decomposition()
        print("composed paths")
        for p in composed_paths:
            print(p)
        max_safe_paths = g.maximal_safe_paths(composed_paths)
        print("maximum safe paths:")
        for p in max_safe_paths:
            print(p)


def read_graph(filename, n=0):  #Ariel: 'n' could have another name such ar number_of_graphs, also, it's strange that the default number of graphs is 0

    str = filename.split('.')

    if str[-1] == 'graph':  #Ariel: The code in this if could be a function called read_graph_format
        graphs = []
        i = 0
        g = nx.DiGraph()
        graph_size = 0
        with open(filename, 'r') as f:
            for line in f:
                if i >= n:
                    break
                read_line = line.rstrip().split(' ')
                if read_line[0] == '#':
                    if graph_size != 0:
                        graphs.append(Graph(g, graph_size))
                    i += 1
                    g = nx.DiGraph()
                    graph_size = 0
                elif len(read_line) == 1:
                    graph_size = int(read_line[0])
                else:
                    g.add_edge(int(read_line[0]), int(
                        read_line[1]), capacity=float(read_line[2]))
                    init_node(g, int(read_line[0]), int(
                        read_line[1]), float(read_line[2]))
        return graphs
    elif str[-1] == 'gfa':  #Ariel: The code in this if could be a function called read_gfa_format
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
                    graph.add_edge(v_from, v_to, capacity=weight)  #Ariel: We could use 'flow' instead of 'capacity'
                    init_node(graph, v_from, v_to, weight)
            return graph


def init_node(graph, v_from, v_to, weight):  #Ariel: These could be 2 functions instead, one called add_flow_in and another add_flow_out
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

#not used


def read_paths(filename):
    paths = []
    with open(filename, 'r') as f:
        for line in f:
            if line[0] == 'P':
                paths.append(line.rstrip())
    return paths


if __name__ == '__main__':
    main()
