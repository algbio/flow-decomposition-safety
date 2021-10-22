'''
Converts sgr/graph file to gfa file.
'''

#!/usr/bin/python3
import argparse
import networkx as nx
from src.scripts import io_helper

def main(filename, mode):
    if mode:
        sgr_to_sg(filename)
    else:
        graphs = io_helper.read_sg_file(filename)
        j = 0
        index_dic = {}
        for graph in graphs:
            i = 1
            for n in list(nx.topological_sort(graph)):
                if n != '(0,0)' and n!='(-1,-1)':
                    graph.nodes[n]['index'] = i
                    index_dic[i] = n
                    i += 1
            graph.nodes['(0,0)']['index'] = 0
            graph.nodes['(-1,-1)']['index'] = len(graph.nodes)-1
            index_dic[0] = '0,0'
            index_dic[len(graph.nodes)-1] = '(-1,-1)'
            print(f'# graph {j} {index_dic}')
            print(len(graph.nodes))
            for n in list(nx.topological_sort(graph)):
                for n1, n2, w in graph.out_edges(n, data=True):
                    print(f'{graph.nodes[n1]["index"]} {graph.nodes[n2]["index"]} {w["weight"]}')
            index_dic = {}

def sgr_to_sg(filename):
    with open(filename, 'r') as f:
        for line in f:
            read = line.rstrip().split()
            if read[0] == '#':
                print(f'H {line.rstrip()}')
            elif len(read) == 3:
                print(f'L\t{read[0]}\t+\t{read[1]}\t+\t{int(float(read[2]))}')
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--file", help="path to file")
    parser.add_argument("-m", "--mode", help="mode of conversion", default=False)
    args = parser.parse_args()
    main(args.file, args.mode)
