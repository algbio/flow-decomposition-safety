#!/usr/bin/python3

def main():
    graph = read_graph('data/genome_graph.gfa')
    print(graph)

def read_graph(filename):
    graph = []
    with open(filename, 'r') as f:
        for line in f:
            if line[0] == 'L':
                graph.append(line.rstrip())
    return graph

    
if __name__ == '__main__':
    main()