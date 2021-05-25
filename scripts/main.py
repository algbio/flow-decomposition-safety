#!/usr/bin/python3

def main():
    file = 'data/dag_graph.gfa'
    graph = read_graph(file)
    # print(graph)
    paths = read_paths(file)
    # print(paths)
    all_max_safe_paths(paths)


def read_graph(filename):
    # save graph as a adjacency list
    graph = {}
    with open(filename, 'r') as f:
        for line in f:
            # read line
            read = ''
            if line.rstrip().count('\t') > 0:
                read = (line.rstrip()).split('\t')
            else:
                read = (line.rstrip()).split(' ')

            # add vertices to graph
            if line[0] == 'S':
                v_index = int(read[1])
                graph[v_index] = []

            # add edge to the adjecency list
            if line[0] == 'L':
                v_from = int(read[1])
                v_to = int(read[3])
                weight = int((read[5])[0:-1])
                graph[v_from].append((v_to, weight))
    return graph


def read_paths(filename):
    paths = []
    with open(filename, 'r') as f:
        for line in f:
            if line[0] == 'P':
                paths.append(line.rstrip())
    return paths

def all_max_safe_paths(paths):
    max_path = ''
    max_flow = 0
    for p in paths:
        parts = p.split(' ')
        weights = parts[3].split(',')
        weights2 = [int(x[0:-1]) for x in weights]
        flow = 9999
        # flow is a minimum of flows of the graph
        for w in weights2:
            if flow > w:
                flow = w
        if flow > max_flow:
            max_flow = flow
            max_path = p
    print(max_path)
    


if __name__ == '__main__':
    main()
